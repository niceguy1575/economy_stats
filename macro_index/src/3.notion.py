#!/usr/bin/python

# setup notion
import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
import requests
import time
from tzlocal import get_localzone


def postUrl(url, headers, data = None, retries=10):
    resp = None

    try:
        resp = requests.post(url, json = data, headers = headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= resp.status_code < 600 and retries > 0:
            print('Retries : {0}'.format(retries))
            return postUrl(url, param, retries - 1)
        else:
            print(resp.status_code)
            print(resp.reason)
            print(resp.request.headers)
    return resp


if __name__ == "__main__":

	# 0. 필요 데이터 setup
	other_path = os.getcwd() + "/data/"
	other_files = os.listdir(other_path)
	data_path = os.getcwd() + "/plot/"
	data = pd.read_csv(data_path + "stat_df.txt", sep = "|")

	now = datetime.now() + timedelta(days=1)
	now_f = now.strftime("%Y-%m-%d")
    
	secret_key = "secret_SzUg5gSUlHSzQthfKAZZk1icFugF3dFypnAc02DN826"
	target_page_id = "07cae222-fb62-4bc5-b402-e96c1c86ed70"
    
	####################################
	# 1. notion page 생성
	####################################
	# 1. 사전에 notion에서 사전에 페이지 획득 필요!
	url = "https://api.notion.com/v1/pages"
	headers = {
		"Accept": "application/json",
		"Notion-Version": "2022-02-22",
		"Content-Type": "application/json",
		"Authorization": "Bearer " + secret_key
	}
	page_data = {
	"parent": { "page_id": target_page_id },
	"properties": {
		"title": {
			"title": [{ "type": "text", "text": { "content": now_f } }]
			}
		},
	"children": [ {
		"object": "block",
		"type": "paragraph",
		"paragraph": {
			"rich_text": [{ "type": "text", "text": { "content": "중요한 미국 경제 지표를 한눈에 살펴볼 수 있는 레포트" } }]
			}
	} ] }
    
	# create page data
	postUrl(url, headers, data = page_data)
	time.sleep(5)

	####################################
	# child block 생성
	####################################
    # 새로 만들어진 page id 확인
	makingID = parent_parse[parent_parse.has_children==True].tail(n = 1).id
	
    ####################################
	# 밑에서부터 작업 진행 (22.03.09~)
    # notion api 화.
	####################################
    
	makingIDchild_page.children.add_new(SubheaderBlock, title = now_f + ' 기준 거시경제 지표 표기')
	child_page.children.add_new(TextBlock, title = ' ')

	# 1. 부도위험
	child_page.children.add_new(HeaderBlock, title = '부도위험')

	child_page.children.add_new(SubheaderBlock, title = 'ICE')
	# 1-1. ice
	ice_value = data.loc[data.label == 'ice'].copy().stat.astype(str).values

	child_page.children.add_new(TextBlock, title = '부도위험 최신값: ' + ice_value[0])
	child_page.children.add_new(TextBlock, title = '부도위험 전월대비 증가율: ' + ice_value[1] + "%")
	child_page.children.add_new(TextBlock, title = '부도위험 전분기대비 증가율: ' + ice_value[2] + "%")
	child_page.children.add_new(TextBlock, title = '부도위험 전년대비 증가율: ' + ice_value[3] + "%")

	# 1-2. ice graph
	child_page.children.add_new(SubsubheaderBlock, title = '부도위험 3month')

	ice_img = child_page.children.add_new(ImageBlock, width=500)
	ice_img.upload_file(data_path + "ICE.png")

	#1-3. ted
	child_page.children.add_new(SubheaderBlock, title = 'TED')

	ted_value = data.loc[data.label == 'ted'].copy().stat.astype(str).values

	child_page.children.add_new(TextBlock, title = 'TED RATE 최신값: ' + ted_value[0])
	child_page.children.add_new(TextBlock, title = 'TED RATE 전월대비 증가율: ' + ted_value[1] + "%")
	child_page.children.add_new(TextBlock, title = 'TED RATE 전분기대비 증가율: ' + ted_value[2] + "%")

	# 1-4. ted graph
	child_page.children.add_new(SubsubheaderBlock, title = 'TED RATE 6month(기준: 1)')
	child_page.children.add_new(TextBlock, title = 'TED Rate: 3개월 리보금리 - 3개월 미국국채금리')

	ted_img = child_page.children.add_new(ImageBlock, width=500)
	ted_img.upload_file(data_path + "TED.png")

	# 1-5. PMI
	child_page.children.add_new(SubsubheaderBlock, title = 'PMI (기준: 50)')

	pmi_img = child_page.children.add_new(ImageBlock, width=500)    
	pmi = re.compile("^PMI")
	pmi_name = list(filter(pmi.search, other_files))[0]
	pmi_img.upload_file(other_path + pmi_name)

	# 1-6. HYG
	child_page.children.add_new(SubsubheaderBlock, title = 'HYG Stock')
	child_page.children.add_new(TextBlock, title = '부도 위험이 낮아질수록 가격이 오르는 주식상품')

	hyg_img = child_page.children.add_new(ImageBlock, width=500)
	hyg_img.upload_file(data_path + "HYG-1month.png")
	
	# 1-7. Libor
	libor_df = pd.read_csv(other_path + "usd_libor.csv", sep = ",")
	
	libor_df.columns = ['label', 'value']
	overnight_libor = str(round(float(libor_df.loc[libor_df.label == 'overnight'].value), 4))
	week1_libor = str(round(float(libor_df.loc[libor_df.label == '1 week'].value), 4))
	month1_libor = str(round(float(libor_df.loc[libor_df.label == '1 month'].value), 4))
	month12_libor = str(round(float(libor_df.loc[libor_df.label == '12 months'].value), 4))
	
	child_page.children.add_new(HeaderBlock, title = '리보 금리')
	child_page.children.add_new(TextBlock, title = '영국 은행끼리 빌리는 돈(콜금리) 비슷')
	child_page.children.add_new(TextBlock, title = '단기 리보금리 > 장기 리보금리 일 경우 위험신호')
	child_page.children.add_new(TextBlock, title = ' ')
	
	child_page.children.add_new(TextBlock, title = '당일 리보금리')
	child_page.children.add_new(TextBlock, title = overnight_libor)
	child_page.children.add_new(TextBlock, title = '1주 리보금리')
	child_page.children.add_new(TextBlock, title = week1_libor)
	child_page.children.add_new(TextBlock, title = '1달 리보금리')
	child_page.children.add_new(TextBlock, title = month1_libor)
	child_page.children.add_new(TextBlock, title = '1년 리보금리')
	child_page.children.add_new(TextBlock, title = month12_libor)
	
	# 1-8. 
	child_page.children.add_new(SubheaderBlock, title = "FOMC 일정")
	child_page.children.add_new(TextBlock, title = '긴급 컨퍼런스 콜 발생 시 위험신호')
	
	fomc_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
	fomc_block = child_page.children.add_new(BookmarkBlock)
	fomc_block.set_new_link(fomc_url)
	
	# 2. 경기
	child_page.children.add_new(HeaderBlock, title = '경기')
	child_page.children.add_new(TextBlock, title = ' ')

	# 2-1. S&P 500
	child_page.children.add_new(SubsubheaderBlock, title = 'S&P 500')

	snp_img = child_page.children.add_new(ImageBlock, width=500)
	snp = re.compile("^p0-37")
	snp_name = list(filter(snp.search, other_files))[0]
	snp_img.upload_file(other_path + snp_name)

	# 2-2. 장단기금리차
	child_page.children.add_new(SubheaderBlock, title = '장단기 금리차')

	t102y = data.loc[data.label == 'ls'].copy().stat.astype(str).values

	child_page.children.add_new(TextBlock, title = '장단기금리차 최신값: ' + t102y[0])
	child_page.children.add_new(TextBlock, title = '장단기금리차 전월대비 증가율: ' + t102y[1] + "%")
	child_page.children.add_new(TextBlock, title = '장단기금리차 전분기대비 증가율: ' + t102y[2] + "%")

	# 2-3. 장단기 금리차 
	child_page.children.add_new(SubsubheaderBlock, title = '장단기 금리차 6개월')

	t102y_img = child_page.children.add_new(ImageBlock, width=500)
	t102y_img.upload_file(data_path + "LS.png")

	# 2-35. 장기금리 추이
	child_page.children.add_new(SubsubheaderBlock, title = '최근 1개월 10 / 20년 장기금리 추이')
	long_mat_img = child_page.children.add_new(ImageBlock, width=500)
	long_mat_img.upload_file(data_path + "long_maturity-1month.png")
	
	# 2-37. Yieldcurve
	child_page.children.add_new(SubsubheaderBlock, title = 'Yield Curve')
	yield_img = child_page.children.add_new(ImageBlock, width=500)
	yield_img.upload_file(data_path + "yield_curve.png")
	
	# 2-4. 미국 기준 금리
	child_page.children.add_new(SubheaderBlock, title = '기준금리')
	fund = data.loc[data.label == 'fund'].stat.astype(str).values

	child_page.children.add_new(TextBlock, title = '기준금리 최신값: ' + fund[0])
	child_page.children.add_new(TextBlock, title = '기준금리 전월대비 증가율: ' + fund[1] + "%")

	# 2-5. 기준금리 그래프
	child_page.children.add_new(SubsubheaderBlock, title = '미국 기준금리 1년')

	fr_img = child_page.children.add_new(ImageBlock, width=500)
	fr_img.upload_file(data_path + "funds_rate.png")

	# 2-6. 미국 실업률
	child_page.children.add_new(SubheaderBlock, title = '실업률')
	ur = data.loc[data.label == 'ur'].stat.astype(str).values

	child_page.children.add_new(TextBlock, title = '실업률 최신값: ' + ur[0])
	child_page.children.add_new(TextBlock, title = '실업률 전월대비 증가율: ' + ur[1] + "%")

	# 2-7. 실업률 그래프
	child_page.children.add_new(SubsubheaderBlock, title = '실업률 6개월')

	fr_img = child_page.children.add_new(ImageBlock, width=500)
	fr_img.upload_file(data_path + "unrate.png")

	# 2-8. 미국물가
	child_page.children.add_new(SubsubheaderBlock, title = '미국 물가 (target: 2%)')

	fr_img = child_page.children.add_new(ImageBlock, width=500)
	fr_img.upload_file(data_path + "price.png")
	
	# 3. 기타 투자 지표
	# 3-1. Fear & Greed Index
	child_page.children.add_new(SubsubheaderBlock, title = 'Fear & Greed Index')
	child_page.children.add_new(TextBlock, title = '40 이하: 시기상 저렴 & 공포')
	child_page.children.add_new(TextBlock, title = '40 <= x <= 60: 중립 ~ 매수 구간')
	child_page.children.add_new(TextBlock, title = '60 이상: 욕심 과열')

	fg_img = child_page.children.add_new(ImageBlock, width=800)
	fg_img.upload_file(other_path + "FG_image.png")

	# 3-2. 경기 사이클 확인
	child_page.children.add_new(SubsubheaderBlock, title = '경기 사이클')
	child_page.children.add_new(TextBlock, title = 'early ~ mid 가 투자 적기!')
	cycle_url = 'https://institutional.fidelity.com/app/item/RD_13569_40890/business-cycle-update.html'
	cycle_block = child_page.children.add_new(BookmarkBlock)
	cycle_block.set_new_link(cycle_url)
	
	# 3-3. roro 지수 확인
	child_page.children.add_new(SubsubheaderBlock, title = 'RORO지수 확인')
	child_page.children.add_new(TextBlock, title = '클수록 위험, 작을수록 공포[=매수타이밍]')
	roro_url = 'https://www.mvis-indices.com/indices/customised/atac-risk-on-risk-off-domestic'
	roro_block = child_page.children.add_new(BookmarkBlock)
	roro_block.set_new_link(roro_url)
	

	print("UPLOADED! " + now_f)
