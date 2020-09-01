from urllib.request import urlopen
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from src.etc.utils.maria_client import get_connection


def fetch_from_naver(code, pages_to_fetch):
    print(f'code : {code}')
    df = None
    try:
        url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
        with urlopen(url) as doc:
            html = BeautifulSoup(doc, 'lxml')
            pgrr = html.find('td', class_='pgRR')
            s = str(pgrr.a['href']).split('=')
            lastpage = int(s[-1])
        df = pd.DataFrame()

        if pages_to_fetch < 0:
            pages_to_fetch = lastpage
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
        df['date'] = df['date'].replace('.', '-')
        df.dropna(inplace=True)
        df[['open', 'close', 'high', 'low', 'diff', 'volume']] = \
            df[['open', 'close', 'high', 'low', 'diff', 'volume']].astype(int)
        df = df[['date', 'open', 'close', 'high', 'low', 'diff', 'volume']]
    except Exception as e:
        print(f'Exception occurred : {e}')
        raise e
    return df


def fetch_target_codes(n_days):
    target_codes = []
    conn = None
    n_days_ago = (datetime.now() - timedelta(hours=n_days)).strftime("%Y-%m-%d")
    qurey = f'''
            SELECT 
                code
            FROM
                company_info 
            WHERE
                last_update > '{n_days_ago}'
            '''
    try:
        conn = get_connection('/srv/stock/config/config.json')
        with conn.cursor() as cs:
            cs.execute(qurey)
            rs = cs.fetchall()
            target_codes = [tup[0] for tup in list(rs)]
    except Exception as ex:
        raise ex
    finally:
        if conn:
            conn.close()
    return target_codes


def upsert_prices():
    query = f"""
        INSERT INTO daily_price
            (code, date, open, close, high, low, diff, volume)
        VALUES
            (%(code)s, %(date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(diff)s, %(volume)s)
        ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            close = VALUES(close),
            high = VALUES(high),
            low = VALUES(low),
            diff = VALUES(diff),
            volume = VALUES(volume)
    """
    target_codes = fetch_target_codes(100)
    batch_size = 200

    for code in list(target_codes):
        mysql_conn = None
        try:
            mysql_conn = get_connection('/srv/stock/config/config.json')
            df = fetch_from_naver(code, -1)
            df['code'] = code
            datalist = df.to_dict(orient='records')
            total_size = len(datalist)
            loops = (total_size // batch_size) + (total_size % batch_size > 0)
            for i in range(1, loops + 1):
                with mysql_conn.cursor() as curs:
                    start = batch_size * i
                    end = (batch_size + 1) * i
                    curs.executemany(query, datalist[start: end])
                mysql_conn.commit()

        except Exception as ex:
            # print(ex)
            # print(f"[Error] Failed to update stock code : {code}")
            raise ex
        finally:
            if mysql_conn:
                mysql_conn.close()


if __name__ == '__main__':
    now = datetime.now()
    print(f"feed_prices starts : {now}")
    upsert_prices()
    now2 = datetime.now()
    print(f"feed_prices ends : {now2}, took {(now2 - now).seconds} s")
