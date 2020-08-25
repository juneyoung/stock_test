import pandas as pd
import pymysql


class MarketDB:
    def __init__(self):
        self.conn = pymysql.connect(host='juneyoung5.cafe24.com', port=3306,
                                    user='jyoh', password='jy85Widerplanet',
                                    db='stock', charset='utf8')

        self.codes = dict()
        self.get_company_info()

    def __del__(self):
        self.conn.close()

    def get_company_info(self):
        sql = """
        SELECT * FROM company_info
        """
        company_info = pd.read_sql(sql, self.conn)
        for idx in range(len(company_info)):
            self.codes[company_info['code'].values[idx]] = company_info['company'].values[idx]

    def get_daily_price(self, code, startDate, endDate):
        sql = f"""
        SELECT 
            * 
        FROM 
            daily_price 
        WHERE 
            code = '{code}' 
            AND date >= '{startDate}' 
            AND date <= '{endDate}'
        """
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df


if __name__ == '__main__':
    print('Run Analyzer')
