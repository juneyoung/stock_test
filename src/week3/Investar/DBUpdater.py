from datetime import datetime
import calendar
from threading import Timer
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import pandas as pd


class DBUpdater:
    def __init__(self):
        company_ddl = """
        CREATE TABLE IF NOT EXISTS company_info (
            code VARCHAR(20),
            company VARCHAR(40),
            last_update DATE,
            PRIMARY KEY (code)
        )
        """

        daily_ddl = """
        CREATE TABLE IF NOT EXISTS daily_price (
            code VARCHAR(20),
            date DATE,
            open BIGINT(20),
            high BIGINT(20),
            low BIGINT(20),
            close BIGINT(20),
            diff BIGINT(20),
            volume BIGINT(20),
            PRIMARY KEY (code, date)
        )
        """

        self.conn = pymysql.connect(host='juneyoung5.cafe24.com', port=3306,
                                    user='jyoh', password='******',
                                    db='stock', charset='utf8')

        with self.conn.cursor() as curs:
            curs.execute(company_ddl)
            curs.execute(daily_ddl)

        self.conn.commit()
        self.codes = dict()
        self.update_comp_info()

    def __del__(self):
        self.conn.close()

    # 이게 클래스 안에 있을 필요는 없지
    def read_krx_code(self):
        url = "https://dev-kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        company_select_sql = """
        SELECT *
        FROM company_info
        """

        select_last_update = """
        SELECT MAX(last_update) 
        FROM company_info
        """

        company_info = pd.read_sql(company_select_sql, self.conn)
        for idx in range(len(company_info)):
            self.codes[company_info['code'].values[idx]] = company_info['company'].values[idx]

        with self.conn.cursor() as curs:
            curs.execute(select_last_update)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] is None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    update_company_info = f"""
                            REPLACE INTO company_info 
                                (code, company, last_update)
                            VALUES
                                ('{code}', '{company}', '{today}')
                            """
                    curs.execute(update_company_info)
                    self.codes[code] = company

                self.conn.commit()

    def read_naver(self, code, company, pages_to_fetch):
        df = None
        try:
            url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
            # anchor 에 붙어있는 href 속성을 가져와서 page 번호 string 을 취득하는 과정
            with urlopen(url) as doc:
                html = BeautifulSoup(doc, 'lxml')
                pgrr = html.find('td', class_='pgRR')
                s = str(pgrr.a['href']).split('=')
                lastpage = s[-1]
            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch)  # 전달받은 페이지보다 최대 페이지가 큰지 확인하는 로직

            for page in range(1, pages + 1):
                pg_url = f'{url}&page={page}'
                df = df.append(pd.read_html(pg_url, header=0)[0])
                df = df.rename(columns={
                    '날짜': 'date',
                    '시가': 'open',
                    '종가': 'close',
                    '고가': 'high',
                    '저가': 'low',
                    '전일비': 'diff',
                    '거래량': 'volume'
                })
                # 수정 종가는?
                df['date'] = df['date'].replace('.', '-')
                df.dropna(inplace=True)
                df[['open', 'close', 'high', 'low', 'diff', 'volume']] = \
                    df[['open', 'close', 'high', 'low', 'diff', 'volume']].astype(int)
                df = df[['date', 'open', 'close', 'high', 'low', 'diff', 'volume']]
        except Exception as e:
            print(f'Exception occurred : {e}')
            raise e
        return df

    def replace_into_db(self, df, num, code, company):
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"""
                REPLACE INTO daily_price 
                VALUES
                ('{code}', '{r.date}', {r.open}, {r.close}, {r.high}, {r.low}, {r.diff}, {r.volume})
                """
                curs.execute(sql)
            self.conn.commit()

    def update_daily_price(self, pages_to_fetch):
        for idx, code in enumerate(self.codes):
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code])

    def execute_daily(self):
        config_file = 'config.json'
        self.update_comp_info()
        try:
            with open(config_file, 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError as fne:
            with open(config_file, 'w') as out_file:
                pages_to_fetch = 100
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch)

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        year = tmnow.year
        month = tmnow.month
        day = tmnow.day
        if tmnow.month == 12 and tmnow.day == lastday:  # 막달의 막일이라면
            year = tmnow.year + 1
            month = 1
            day = 1
        elif tmnow.day == lastday:
            month = tmnow.month + 1
            day = 1
        else:
            day = tmnow.day + 1
        tmnext = tmnow.replace(year=year, month=month, day=day, hour=17, minute=0, second=0)
        tmdiff = (tmnext - tmnow).seconds
        t = Timer(tmdiff, self.execute_daily)
        t.start()


if __name__ == '__main__':
    print('DB Updater')
    updater = DBUpdater()
    updater.execute_daily()
