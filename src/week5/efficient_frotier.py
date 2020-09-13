import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.week3.Investar.Analyzer import Analyzer

open_days = 252
portfolio_count = 20000

if __name__ == '__main__':
    market_db = Analyzer()
    stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
    start_dt = '2016-01-01-04'
    end_dt = '2018-04-27'

    df = pd.DataFrame()
    for stock in stocks:
        df[stock] = market_db.get_daily_price_with_name(stock, start_dt, end_dt)['close']

    daily_ret = df.pct_change()  # 일간 변동률
    annual_ret = daily_ret.mean() * open_days  # 연간 수익률
    daily_cov = daily_ret.cov()   # 일간 리스크(공분산)
    annual_cov = daily_cov * open_days  # 연간 리스크

    port_ret = []
    port_risk = []
    port_weights = []
    sharp_ratio = []

    for _ in range(portfolio_count):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)  # weights 에 할당된 모든 엘리먼트를 웨이트의 총합으로 나눔

        # 가중합 : https://rfriend.tistory.com/tag/np.dot%28%29 <= 좀 복잡함
        returns = np.dot(weights, annual_ret)  # np.dot 이나 matmul 로 가중합을 구한다. => 행렬 곱
        # 잘 이해 안감. 물어보기 => 연간 공분산과 종복별 비중 곱(ok) + 종목별 비중의 전치로 곱(?)
        # + 제곱근 하면 전체리스크라고 ???
        risks = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

        port_ret.append(returns)
        port_risk.append(risks)
        port_weights.append(weights)
        # 샤프 지수
        sharp_ratio.append(returns/risks)

    portfolio = {'returns': port_ret, 'risks': port_risk, 'sharp': sharp_ratio}

    for idx, stock_name in enumerate(stocks):
        portfolio[stock_name] = [weight[idx] for weight in port_weights]  # 종목별 가중치 배열

    portfolio_dataframe = pd.DataFrame(portfolio)
    print(portfolio_dataframe.head(5))
    # 데이터프레임의 칼럼은 returns, risks, ...종목 이름 이다
    # portfolio_dataframe[['returns', 'risks'] + [stock_name for stock_name in stocks]]
    portfolio_dataframe[['returns', 'risks', 'sharp'] + [stock_name for stock_name in stocks]]

    # 효율적 투자선보다 높은 소득을 기대하기 어려움
    # 투자선 내에서 최적의 지점을 찾는 방법 => 샤프 지수
    # 예상 수익률 - 무위험률 / 수익률의 표준편차  #  ?? 무위험률 ??
    # 샤프지수 == high risk, high return
    max_sharp = portfolio_dataframe.loc[portfolio_dataframe['sharp'] == portfolio_dataframe['sharp'].max()]
    min_risk = portfolio_dataframe.loc[portfolio_dataframe['risks'] == portfolio_dataframe['risks'].min()]

    print(f'max_sharp : {max_sharp}')
    print(f'min_risk : {min_risk}')

    portfolio_dataframe.plot.scatter(x='risks', y='returns', c='sharp'
                                     , cmap='viridis', edgecolors='k', figsize=(11, 7), grid=True)
    plt.scatter(x=max_sharp['risks'], y=max_sharp['returns'], c='r', marker='*', s=300)  # 하이리스크 하이리턴
    plt.scatter(x=min_risk['risks'], y=min_risk['returns'], c='r', marker='X', s=200)  # 안전빵
    plt.title('Efficient Frontier')
    plt.xlabel('Risk')
    plt.ylabel('Expected Returns')
    plt.show()
