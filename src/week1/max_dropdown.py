import pandas as pd
from scipy import stats
import yfinance
# from pandas_datareader import data as pdr
import pandas_datareader as pdr
import matplotlib.pyplot as plt


def get_data(stock_name, start, end):
    return pdr.get_data_yahoo(stock_name, start=start, end=end)


if __name__ == '__main__':
    yfinance.pdr_override()
    start_date = '2019-01-01'
    end_date = '2019-12-31'
    df1_id = '^KS11'
    # df1_id = '060250.KQ'
    df2_id = '^DJI'
    df1 = get_data(df1_id, start_date, end_date)
    df2 = get_data(df2_id, start_date, end_date)
    window = 252  # 기간으로 1년 중 개장일이 252 일이라는 가정
    # min_period 는 데이터의 갯수가 window 에 못미치더라도 만족하면 작업을 수행할 최소수
    peak = df1['Adj Close'].rolling(window, min_periods=1).max()  # 최고가는 MAX
    dd = df1['Adj Close']/peak - 1.0  # dropdown 은 최고치 대비 현재 종가
    max_dd = dd.rolling(window, min_periods=1).min()  # 종가 중 최저치

    # figsize 차트의 가로인치, 세로인치
    plt.figure(figsize=(9, 7))

    # 화면에 여러플롯을 나눠서 그리는 기능
    plt.subplot(211)  # 2행 1열 1행?
    df1['Close'].plot(label=df1_id, title=f"{df1_id} MDD", grid=True, legend=True)
    plt.subplot(212)
    dd.plot(c='blue', label=f"{df1_id} DD", grid=True, legend=True)
    max_dd.plot(c='red', label=f"{df1_id} MDD", grid=True, legend=True)
    plt.show()
