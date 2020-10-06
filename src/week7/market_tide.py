# 삼중창의 첫째 창
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates  # ?
from src.week3.Investar.Analyzer import Analyzer


if __name__ == '__main__':
    print(f"First Screen = Market Tide")
    market_db = Analyzer()
    stock_dataframe = market_db.get_daily_price_with_name('SK하이닉스', '2018-11-01', '2019-09-10')

    # ewm 을 이용한 이평선 구하기
    # https://www.openaitrading.com/python-pandas-%EC%9D%B4%EB%8F%99%ED%8F%89%EA%B7%A0-%EA%B5%AC%ED%95%98%EA%B8%B0/
    ema60 = stock_dataframe.close.ewm(span=60).mean()  # 지수 이평선
    ema130 = stock_dataframe.close.ewm(span=130).mean()  # 26 주
    mcda = ema60 - ema130

    signal = mcda.ewm(span=45).mean()
    mcdahist = mcda - signal

    # 새로운 칼럼 추가
    new_df = stock_dataframe.assign(ema130=ema130, ema60=ema60, mcda=mcda, signal=signal, mcdahist=mcdahist).dropna()
    new_df['number'] = new_df.index.map(mdates.date2num)
    ohlc = new_df[['number', 'open', 'high', 'low', 'close']]

    plt.figure(figsize=(9, 7))
    p1 = plt.subplot(2, 1, 1)
    plt.title('First Screen : Market Tide')
    plt.grid(True)

    candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
    p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.plot(new_df.number, new_df['ema130'], color='c', label='EMA130')
    plt.legend(loc='best')

    p2 = plt.subplot(2, 1, 2)
    plt.grid(True)
    p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.bar(new_df.number, new_df['mcdahist'], color='m', label='MCDA HISTOGRAM')
    plt.plot(new_df.number, new_df['mcda'], color='b', label='MCDA')
    plt.plot(new_df.number, new_df['signal'], 'g--', label='MCDA-Signal')
    plt.legend(loc='best')

    plt.show()
