import pandas as pd
from scipy import stats
import yfinance
# from pandas_datareader import data as pdr
import pandas_datareader as pdr
import matplotlib.pyplot as plt


def get_data(stock_name, start, end):
    return pdr.get_yahoo_data(stock_name, start=start, end=end)


if __name__ == '__main__':
    yfinance.pdr_override()
    start_date = '2019-01-01'
    end_date = '2019-12-31'
    df1_id = '^K11'
    df2_id = '^DJI'
    df1 = get_data(df1_id, start_date, end_date)
    df2 = get_data(df2_id, start_date, end_date)


    window = 252  # 기간으로 1년 중 개장일이 252 일이라는 가정
    peak = df1['Adjust Close'].rolling(window, min_periods=1).max()  # 최고가는 MAX
    dd = df1['Adjust Close']/peak - 1.0  # dropdown 은 최고치 대비 현재 종가
    max_dd = dd.rolling(window, min_periods=1).min()  # 종가 중 최저치

    plt.figure(figsize=(9, 7))
    plt.subplot(211)  # 2행 1열 1행?
    df1['Close'].plot(label=df1_id, title=f"{df1_id} MDD", grid=True, legend=True)
    plt.subplot(212)
    dd.plot(c='blue', label=f"{df1_id} DD", grid=True, legend=True)
    max_dd.plot(c='red', label=f"{df1_id} MDD", grid=True, legend=True)
    plt.show()
