from urllib.request import urlopen
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from src.etc.utils.maria_client import get_connection


def fetch_from_naver(code, pages_to_fetch):
    df = None
    try:
        url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
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
            target_codes = list(rs)
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
        ON DUPLICATED KEY 
            open = %(open)s,
            close = %(close)s,
            high = %(high)s,
            low = %(low)s,
            diff = %(diff)s,
            volume = %(volume)s
    """

    target_codes = fetch_target_codes(100)
    for code in list(target_codes):
        print(code)
    pass


if __name__ == '__main__':
    now = datetime.now()
    print(f"feed_prices starts : {now}")
    upsert_prices()
    now2 = datetime.now()
    print(f"feed_prices ends : {now2}, took {(now2 - now).seconds} s")
