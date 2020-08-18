from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

"""
    pip3 install beautifulsoup4
    pip3 install lxml
    
    lxml : flexible and fast
    html5lib : parser for complex html
"""

if __name__ == '__main__':
    stock_code = '090430'
    url_for_stock_basic = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}'
    url_for_stock_test = f'{url_for_stock_basic}&page=1'
    last_page = 1

    df = pd.DataFrame()

    # parse html than read the last page
    with urlopen(url_for_stock_test) as doc:
        html = BeautifulSoup(doc, 'lxml')
        pgrr = html.find('td', class_='pgRR')
        s = str(pgrr.a['href']).split('=')
        last_page = s[-1]

    for i in range(1, int(last_page) + 1):
        # What is this "header" for ? why use only index 0 ?
        df = df.append(pd.read_html(f'{url_for_stock_basic}&page={i}', header=0)[0])

    df.dropna(inplace=True)  # check case of NaN
    print(df.head())
