from urllib.request import urlopen
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from src.etc.utils.maria_client import get_connection
import pymysql
"""
1. stock 디비에서 종목 전부 가져오기
2. nhn 에서 종목별 가격 가져오기 = too long
3. 저장 

"""


def fetch_max_page(code):
    lastpage = 0
    url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
    with urlopen(url) as doc:
        html = BeautifulSoup(doc, 'lxml')
        pgrr = html.find('td', class_='pgRR')
        s = str(pgrr.a['href']).split('=')
        lastpage = int(s[-1])
    return lastpage


def fetch_from_naver(code, start_page, end_page):
    print(f'code : {code}')
    df = pd.DataFrame()
    url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
    for page in range(start_page, end_page):
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
    df['code'] = code
    return df


def fetch_target_codes(n_days):
    target_codes = []
    conn = None
    n_days_ago = (datetime.now() - timedelta(days=n_days)).strftime("%Y-%m-%d")
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
    """

    # query = f"""
    #     INSERT INTO daily_price
    #         (code, date, open, close, high, low, diff, volume)
    #     VALUES
    #         (%(code)s, %(date)s, %(open)s, %(close)s, %(high)s, %(low)s, %(diff)s, %(volume)s)
    #     ON DUPLICATE KEY UPDATE
    #         open = VALUES(open),
    #         close = VALUES(close),
    #         high = VALUES(high),
    #         low = VALUES(low),
    #         diff = VALUES(diff),
    #         volume = VALUES(volume)
    # """
    # target_codes = fetch_target_codes(100)
    target_codes = ['000660', '005930', '005380', '035420']  # SK하이닉스, 삼성전자, 현대차, NAVER

    for code in list(target_codes):
        max_stock_pages = fetch_max_page(code)
        pages_per_df = 20
        df_loops = (max_stock_pages // pages_per_df) + (max_stock_pages % pages_per_df > 0)
        for page in range(df_loops):
            start_dt = datetime.now()
            start = (page * pages_per_df) + 1
            end = start + pages_per_df - 1
            print(f"code : {code}, pages from {start} to  {end}, begin : {start_dt}")
            df = fetch_from_naver(code, start, end)
            datalist = df.to_dict(orient='records')
            try:
                mysql_conn = get_connection('/srv/stock/config/config.json')
                with mysql_conn.cursor() as curs:
                    curs.executemany(query, datalist)
                mysql_conn.commit()
            except pymysql.err.IntegrityError as ie:
                pass
            except Exception as ex:
                raise ex
            finally:
                end_dt = datetime.now()
                print(f"code : {code}, pages from {start}, end : {start_dt}, took : {(end_dt - start_dt).seconds} s")
                if mysql_conn:
                    mysql_conn.close()


if __name__ == '__main__':
    now = datetime.now()
    print(f"feed_prices starts : {now}")
    upsert_prices()
    now2 = datetime.now()
    print(f"feed_prices ends : {now2}, took {(now2 - now).seconds} s")
