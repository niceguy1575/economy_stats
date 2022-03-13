# '미국주식' 투자를 위한 지표 모니터링 프로그램

본 프로그램은 다음의 목표를 가지고 있습니다.
  
## 오늘의 경제 리포트

👉 미국 경제 지표를 일 단위로 수집하고 notion에서 모니터링 하기 위한 목표를 가지고 있습니다.
주요 활용 프로그램은 python이며 notion-py 패키지를 적극적으로 활용했습니다. 

상세 수행 내역은 다음과 같습니다.

1. FRED 등 다양한 미국 경제 지표 수집
2. 관심 통계 자료 생성
3. notion upload

예시: https://niceguy1575.notion.site/2022-03-13-d87cd06f268f4c0fa220982dddc19b15

### 실행방법
~~~
# on command
1. git clone 및경로로 파일 이동
2. sh run.sh

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

6. Yield Curve

https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldYear&year=2021

7. USD Libor

https://www.global-rates.com/en/interest-rates/libor/american-dollar/american-dollar.aspx

## 업데이트 항목
1. notion official api로 동작 업데이트 
2. 불필요한 정보 제외 / 꼭 확인해야하는 지표 위주로 리포트 구성
3. 리포트 결과 메일로 송부

