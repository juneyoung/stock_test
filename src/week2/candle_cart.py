from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from datetime import datetime
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc

base_url = 'https://finance.naver.com/item/sise_day.nhn'


def fetch_last_page(stock_code):
    last_page = 1
    with urlopen(f'{base_url}?code={stock_code}') as doc:
        html = BeautifulSoup(doc, 'lxml')
        pgrr = html.find('td', class_='pgRR')
        s = str(pgrr.a['href']).split('=')
        last_page = s[-1]
    return last_page


def crawling_data(stock_code, start=1, end=5):
    df = pd.DataFrame()
    for i in range(start, int(end) + 1):
        df = df.append(pd.read_html(f'{base_url}?code={stock_code}&page={i}', header=0)[0])
    df.dropna(inplace=True)
    df.sort_values(by='날짜')
    print(df.head())
    return df


def draw_line_chart(stock_code, df):
    plt.title(f'Stock(close) : {stock_code}')
    plt.xticks(rotation=45)  # ?
    plt.plot(df['날짜'], df['종가'], 'co-')
    plt.grid(color='gray', linestyle='--')
    return plt


def draw_candle_chart(stock_code, df):
    for idx in range(len(df)):
        dt = datetime.strptime(df['날짜'].values[idx], '%Y.%m.%d').date()
        df['날짜'].values[idx] = mdates.date2num(dt)

    ohlc = df[['날짜', '시가', '고가', '저가', '종가']]
    plt.figure(figsize=(9, 6))
    ax = plt.subplot(1, 1, 1)
    plt.title(f'{stock_code} candle chart')
    candlestick_ohlc(ax, ohlc.values, width=.7, colorup='red', colordown='blue')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.grid(color='gray', linestyle='--')
    return plt


def draw_candle_chart2(stock_code, df, type_='ohlc'):
    df = df.rename(columns={'날짜': 'Date', '시가': 'Open', '고가': 'High', '저가': 'Low', '종가': 'Close', '거래량': 'Volume'})
    df = df.sort_values(by='Date')
    df.index = pd.to_datetime(df.Date)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    mpf.plot(df, title=f'{stock_code} OHLC', type=type_)


if __name__ == '__main__':
    stock = '090430'
    last_page = fetch_last_page('090430')
    df = crawling_data(stock, end=last_page)
    # draw_candle_chart(stock, df.iloc[0:30]).show()
    # draw_line_chart(stock, df.iloc[0:30]).show()
    draw_candle_chart2(stock, df.iloc[0:30])
    # draw_candle_chart2(stock, df.iloc[0:30], type_='candle')
