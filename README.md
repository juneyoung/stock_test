## 시스템 매매 스터디



### 00. 개요
 
시스템 매매로 대량의 데이터 처리와 분석에 대해 스터디

책
-  파이썬 증권 데이터 분석, 한빛 미디어 (김황후 저)
-  파이썬으로 배우는 알고리즘 트레이딩, 위키북스 (조대표 저)

방향성
- 내가 내 자신을 알건데, 재미없으면 안하니까 결과물 나오는 거 먼저하고 부족하면 돌아가기
- 투자보다는 분석을 잘하고 싶음 

### 2020 08 첫째주
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

### 2020 08 둘째주
#### 파이썬 증권 데이터 분석 (p.174 ~ p.203) + Windows Setting

##### 준비물
```
$> pipenv install beautifulsoup4
$> pipenv install lxml
$> pipenv install mplfinance
```
mplfinance 라이브러리 OSX 설치시, dependencies 관련 경고가 발생하는데, 무시하고 진행하는데 이슈가 없었음. 

##### Main Contents
- Beautiful soup & lxml
- Japanese Candle Chart(미국식은 mplfinance 의 디폴트 차트 모양)

##### 캔들 차트

- 적색 : 상승장. "양봉" 혹은 bullish. 세로선으로 High 와 Low 를 나타내고, 몸통으로 종가와 시가를 나타냄
- 청색 : 하락장. "음봉" 혹은 bearish. 세로선으로 High 와 Low 를 나타내고, 몸통으로 시가와 종가를 나타냄(몸통만 상승장과 반대)

##### 주의점 

- `mplfinance` 의 `plot` 에서 자동으로 칼럼을 탐지하지만 정확히 칼럼명이 맞아야 인지함(`Open`(O), `open`(X))

##### Trouble shooting

오류 01 : OSX 에서 `urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)>`
```
$> /Applications/Python\ 3.8/Install\ Certificates.command
```

오류 02. Windows 에서 `msvcr100.dll 가 없어...`
```
Visual C++ 재배포 가능 패키지 설치
```

### 2020셋 08월 셋째주
#### 파이썬 증권 데이터 분석 (p.208 ~ p.251)
#### cafe24 호스팅 신청

business 용으로 신청했음

아래 작업들을 수행하였음

- groupadd
- useradd
- sudoers 등록
- firewalld activate
- yum update
- openjdk-11.0.8-devel 설치
- mariadb 설치 + (charset 변경 / 권한 관리)
- python3.8.5 [설치](https://computingforgeeks.com/how-to-install-python-on-3-on-centos/)

```
등록된 사용자 조회 
$> cat /etc/passwd
등록된 그룹 조회
$> cat /etc/group
# 그룹 추가 
$> groupadd guests
# 사용자 추가
$> useradd -g guests guest1
$> passwd guest1
```

sudoers file 에 그룹 단위로 권한을 줄 때는 `%` 를 사용한다. `sudoers` 파일에서 ... 
```
%guests ALL=(ALL) ALL
```

#### 주요 내용
- try except
- UPSERT 를 구현하는 방법 
    - `REPLACE INTO table VALUES (values)` 구문 
    - `INSERT INTO table (columns) VALUES (values) ON KEY DUPLICATED UPDATE column=value, ... ` 구문
- Timer 는 timedelta 와 callable 을 받아 수행함





### 2020셋 09월 둘째주
#### 파이썬 증권 데이터 분석 (p.254 ~ p.275)

#### 주요 내용
- 공분산을 활용한 risk 계산
- 수익률 == 변동률 ?
- 샤프지수 = 예상 수익률 - 무위험률 / 수익률의 표준편차 => 수익률 대비 리스크가 높은 지점 찾기
- 볼린저밴드
  - 20 일 기준
  - 상단 밴드 : 상대적 고점. 중간 밴드 + 2*표준편차 
  - 하단 밴드 : 상대적 저점. 중간 밴드 - 2*표준편차 
  - 폭이 넓을 수록 변동성이 강한 종목 
- 볼린저밴드 지표
  - 하단밴드는 0.0, 상단밴드는 1.0 
  - (종가 - 하단밴드) / (상단밴드 - 중단밴드)
- 스퀴즈(squeeze)
  - 변동폭이 너무 낮아서 곧 변동성이 오를 상황
  - 배드폭으로 구함: (상단밴드 - 하단밴드) / 중단 밴드 


#### Q
아니 쓰레드 돌릴라고 데이터베이스 Timeout 을 80시간으로 설정하는게 말이 되나...  


### 테스트용
겁나 멀었음...
