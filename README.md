# '미국주식' 투자를 위한 지표 모니터링 프로그램

본 프로그램은 다음의 목표를 가지고 있습니다.

## 1. macro_index
👉 미국 경제 지표를 일 단위로 수집하고 notion에서 모니터링 하기 위한 목표를 가지고 있습니다.
주요 활용 프로그램은 python이며 notion-py 패키지를 적극적으로 활용했습니다. 

상세 수행 내역은 다음과 같습니다.

1. FRED 등 다양한 미국 경제 지표 수집
2. 관심 통계 자료 생성
3. notion upload

예시: https://www.notion.so/niceguy1575/2020-10-08-0e39c38529de4eb4a4732efa6d1a2a44

### 실행방법
1. git clone
2. macro_index/run 경로로 이동
3. bash 명령어 실행: **./economy_run.sh**

## 2. stock_index
👉 미국 개별 주식의 데이터에 관련한 개괄적인 분석을 하기 위한 목표를 가지고 있습니다.
기업에 대한 개괄적인 정보 및 성장성, 거래규모, 유용한 정보를 담은 사이트로 연결해줍니다.

상세 수행 내역은 다음과 같습니다.
1. yahoo finance 기준 데이터 수집 및 표기
2. 성장성 및 거래규모 분석

예시: https://www.notion.so/niceguy1575/2020-10-13-a16f8fe1d31e4ba9a68468cb9816f25b

### 실행방법
~~~
# on command
1. git clone
2. stock_index/run
3. bash 명령어 실행: **./stock_run.sh**

# click in mac
1. 더블클릭: ./run_on_mac/0.0.run_all.command
~~~

## 활용 패키지 목록 및 참고

~~~ python
# used packages
packages = ['yfinance', 'pandas', 'requests', 're', 'numpy', 'matplotlib', 'PyMuPDF', 'notion', 'bs4', 'datetime', 'dateutil', 'fitz']
~~~

💁‍♀️ 페이스북 노션 홈페이지 홍보: [http://asq.kr/79zMEd5c0ri2](http://asq.kr/79zMEd5c0ri2)

😊 참고 강의: http://frindle.co.kr// 


## 참고 site

1. FRED

    [https://fred.stlouisfed.org/](https://fred.stlouisfed.org/)
    [https://fred.stlouisfed.org/docs/api/fred/](https://fred.stlouisfed.org/docs/api/fred/)

2. US PMI

    [https://tradingeconomics.com/united-states/business-confidence](https://tradingeconomics.com/united-states/business-confidence)

3. S&P 500 12 fwd eps

    [https://insight.factset.com/sp-500-forward-p/e-ratio-rises-above-20.0-as-eps-estimates-continue-to-fall](https://insight.factset.com/sp-500-forward-p/e-ratio-rises-above-20.0-as-eps-estimates-continue-to-fall)

4. notion py

    [https://github.com/jamalex/notion-py](https://github.com/jamalex/notion-py)

5. Fear & Greed Index 

    [https://money.cnn.com/data/fear-and-greed/](https://money.cnn.com/data/fear-and-greed/)

## 수정사항

21.01.23
~~~
1. gcp 환경에서 mac local환경으로 이전
2. 더블클릭으로 실행할 수 있도록 수정
3. 데이터 수집 url 수정 및 수집 주식 범위 변경
~~~


## 향후 보안사항
1. 주식 관련 알람
