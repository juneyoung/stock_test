from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from matplotlib import pyplot as plt

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
    print(df.head())
    return df


def draw_chart1(stock_code, df):
    plt.title(f'Stock(close) : {stock_code}')
    plt.xticks(rotation=45)  # ?
    plt.plot(df['날짜'], df['종가'], 'co-')
    plt.grid(color='gray', linestyle='--')
    return plt


if __name__ == '__main__':
    stock = '090430'
    last_page = fetch_last_page('090430')
    df = crawling_data(stock, end=last_page)
    draw_chart1(stock, df).show()
