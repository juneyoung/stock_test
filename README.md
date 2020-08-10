## 시스템 매매 스터디



### 00. 개요
 
시스템 매매로 대량의 데이터 처리와 분석에 대해 스터디

책
-  파이썬 증권 데이터 분석, 한빛 미디어 (김황후 저)
-  파이썬으로 배우는 알고리즘 트레이딩, 위키북스 (조대표 저)

방향성
- 내가 내 자신을 알건데, 재미없으면 안하니까 결과물 나오는 거 먼저하고 부족하면 돌아가기
- 투자보다는 분석을 잘하고 싶음 

### 202008 첫째주
#### 파이썬 증권 데이터 분석 (p.142 ~ p.171)

##### 준비물
```
$> pipenv install yfinance
$> pipenv install pandas-datareader
$> pipenv install pandas scipy
$> pipenv install matplotlib
```

[yfinance](https://finance.yahoo.com/)에서 주식 구분자를 구해서 기간 내 OHLC + Adjust Close, Volume 을 얻을 수 있음
```
import yfinance as yf
import pandas_datareader as pdr

yf.pdr_override()
pdr.get_data_yahoo('^DJI', start='2020-01-01')
```

- `end` 조건을 주지 않으면 해당 기간부터 현재까지 다 가져오기 때문에 매우 오래 걸림
- `pdr_override` 하면 좀 빠르다고 함. ([yfinance 깃헙](https://github.com/ranaroussi/yfinance)) 

##### 주요 내용

- `Daily Percent Change` 구하기 : `shift` method, `pct_change` method
- 일간 변동률의 `Cumumlative Sum` 구하기 : `cumsum` method
- `Maximum Dropdown` 구하기 : `rolling` method
- 기준이 달라서 비교가 힘들 때는 지수 비교로(특정 일자를 기준으로 변량을 구해서 비교)
- 산점도 비교 : `inplace` 키워드
- 상관계수와(`r-value`) 결정계수(`r-squad`) : `corr` method. 결정 계수는 상관 계수의 제곱, 1 에 가까울 수록 예측치가 회귀선에 일치
- 포트폴리오는 음의 상관계수를 가진 종목으로!

##### Q
- kopsi 와 dow, samsung 과 google 을 비교하는데 왜 한국 주식의 종가만 `-1` 을 하는지? (`p.152`, `p.154`)
- shift 연산해서 빼는 것과 `pct_change` 는 다른가?
- 일간 변화율이 있는데 `cumsum` 을 구하는 이유는 뭣 때문이지?

##### 그외
- `end` 조건이 달라서 그런지 산점도 등을 그려보면 책과 꽤나 다른 그래프가 짠!
- `NHN KCP CORP` 같은 주식도 `yfinance` 에 있는데 기간을 줘도 하루치 밖에 조회 안됨
