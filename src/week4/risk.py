import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.week3.Investar import Analyzer


if __name__ == '__main__':
    mk = Analyzer.Analyzer()
    stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER', '녹십자홀딩스']
    df = pd.DataFrame()
    for s in stocks:
        # df[s] = mk.get_daily_price_with_name(s, '2016-01-04', '2018-04-27')['close']
        df[s] = mk.get_daily_price_with_name(s, '2020-08-11', '2020-08-25')['close']

    print(df.head(5))
    daily_ret = df.pct_change()  # 일간 수익률
    annual_ret = daily_ret.mean() * 252  # 연간 수익률
    daily_cov = daily_ret.cov()  # 일간 리스크
    annual_cov = daily_cov * 252  # 연간 리스크

