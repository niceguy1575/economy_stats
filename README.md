# notion을 활용한 경제 지표 모니터링

미국 경제 지표를  일 단위로 수집하고 notion에서 모니터링 하기 위한 목표를 가지고 있습니다.

주요 활용 프로그램은 python이며 notion-py 패키지를 적극적으로 활용했습니다. 

상세 수행 내역은 다음과 같습니다.

1.  FRED 등 다양한 미국 경제 지표 수집
2. 관심 통계 자료 생성
3.  notion upload

## 실행방법
1. git clone 및 경로로 이동
2. bash 명령어 실행: **./run/economy_run.sh**

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

1. 채권관련 index 추가
2. 리보금리기반 장단기 금리차 확인
3. 회사채 내용 반영

