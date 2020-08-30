from datetime import datetime
import pandas as pd
from src.etc.utils.maria_client import get_connection


def fetch_krx():
    url = "https://dev-kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
    krx = pd.read_html(url, header=0)[0]
    krx = krx[['종목코드', '회사명']]
    krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
    krx.code = krx.code.map('{:06d}'.format)
    return krx


def upsert_stocks ():
    conn = None
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        conn = get_connection('/srv/stock/config/config.json')
        krx = fetch_krx()
        with conn.cursor() as curs:
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
    except Exception as ex:
        raise ex
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    now = datetime.now()
    print(f"feed_stocks starts : {now}")
    upsert_stocks()
    now2 = datetime.now()
    print(f"feed_stocks ends : {now2}, took {(now2 - now).seconds} s")
