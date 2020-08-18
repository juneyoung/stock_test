import pandas as pd
from scipy import stats
import yfinance
import pandas_datareader as pdr
import matplotlib.pyplot as plt


def get_data(stock_name, start, end):
    return pdr.get_data_yahoo(stock_name, start=start, end=end)


if __name__ == '__main__':
    start_date = '2018-05-04'
    end_date = '2019-09-06'
    id1 = '005930.KS'
    id2 = 'MSFT'
    df1 = get_data(id1, start_date, end_date)
    df2 = get_data(id2, start_date, end_date)
    df1_dpc = (df1.Close - df1.Close.shift(1)) / df1.Close.shift(1) * 100
    # df2_dpc = (df2.Close - df2.Close.shift(1)) / df2.Close.shift(1) * 100
    df2_dpc = (df2.Close - df2.Close.shift(1) / df2.Close.shift(1) - 1) * 100

    df1_dpc.iloc[0] = 0
    df2_dpc.iloc[0] = 0

    # plt.hist(df1_dpc, bins=18)
    # plt.show()

    df1_dpc1 = df1.Close.pct_change()
    # 비슷도 안함
    print(f"pct_change : {df1_dpc1.head()}")
    print(f"calced : {df1_dpc.head()}")

    # 누적합
    cs1 = df1_dpc.cumsum()
    cs2 = df2_dpc.cumsum()

    # plt.subplot(211)
    plt.plot(df1.index, cs1, 'b', label=f"{id1}")
    plt.plot(df2.index, cs2, 'r--', label=f"{id2}")
    plt.ylabel('Change % cumsum')
    plt.grid(True)
    plt.legend(loc='best')

    # plt.subplot(212)
    # plt.plot(df1.index, df1_dpc, 'b', label=f"{id1}")
    # plt.plot(df2.index, df2_dpc, 'r--', label=f"{id2}")
    # plt.ylabel('Change %')
    # plt.grid(True)
    # plt.legend(loc='best')

    plt.show()

    # 100, 150, 300
    d1 = pd.DataFrame({'c': [100, 150, 300]})
    d2 = d1.pct_change()
    print(f"cusum : {d2.cumsum()}")
