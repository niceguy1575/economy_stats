# notion을 활용한 경제 지표 모니터링

미국 경제 지표를  일 단위로 수집하고 notion에서 모니터링 하기 위한 목표를 가지고 있습니다.

주요 활용 프로그램은 python이며 notion-py 패키지를 적극적으로 활용했습니다. 

상세 수행 내역은 다음과 같습니다.

1. FRED 등 다양한 미국 경제 지표 수집
2. 관심 통계 자료 생성
3. notion upload

## 실행방법
1. git clone 및 run 경로로 이동
2. bash 명령어 실행: **./economy_run.sh**

### 활용 패키지 목록

- pandas
- requests
- re
- numpy
- matplotlib
- PyMuPDF
- notion

💁‍♀️ 페이스북 노션 홈페이지 홍보: [http://asq.kr/79zMEd5c0ri2](http://asq.kr/79zMEd5c0ri2)

😊 참고 강의: http://frindle.co.kr/

예시 URL: https://www.notion.so/niceguy1575/2020-10-08-0e39c38529de4eb4a4732efa6d1a2a44

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

## 향후 보안사항

1. greed & fear index
2. 부도위험주 반영
3. USD Libor금리 1일금리 > 1년금리
4. TED 3개월 리보금리 - 3개월 미국국채금리
5. hyg ⇒ 부도위험 etf, 부도위험 내려가면 가격이 오름.
6. 채권관련 index 추가
