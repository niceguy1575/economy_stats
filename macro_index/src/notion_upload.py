#!/usr/bin/python

# setup notion
import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import ImageBlock
from notion.block import HeaderBlock
from notion.block import SubheaderBlock
from notion.block import SubsubheaderBlock
from notion.block import PageBlock
import time

# main definition
if __name__ == "__main__":
	
	# get token
	niceguy_token = "ed06a3b886caad4a1cb7c8b5aad08d016ba6efe6b60223a686dbcc900ed147043b30c130a0eb5197e6fb3cb4ba113bc03e532d6ca23527d92ca43b4f19de5de36d386a3664e20b3600c49dce2dbc"
	client = NotionClient(token_v2 = niceguy_token)
	page = client.get_block("https://www.notion.so/niceguy1575/07cae222fb624bc5b402e96c1c86ed70")

	now = datetime.now() + timedelta(days=1)
	now_f = now.strftime("%Y-%m-%d")
	page.children.add_new(PageBlock, title=now_f)

	# data load
	other_path = os.getcwd() + "/data/"
	other_files = os.listdir(other_path)
	data_path = os.getcwd() + "/plot/"
	data = pd.read_csv(data_path + "stat_df.txt", sep = "|")

	time.sleep(5)

	####################################
	# 맨 마지막 page에 내용 추가
	####################################
	child_id = [c.id for c in page.children][-1]

	child_page = client.get_block(child_id)

	child_page.children.add_new(SubheaderBlock, title = now_f + ' 기준 거시경제 지표 표기')
	child_page.children.add_new(TextBlock, title = ' ')

	print("1. 부도위험")
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
	print("2. ted")
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
	print("3. PMI")
	child_page.children.add_new(SubsubheaderBlock, title = 'PMI (기준: 50)')

	pmi_img = child_page.children.add_new(ImageBlock, width=500)    
	pmi = re.compile("^PMI")
	pmi_name = list(filter(pmi.search, other_files))[0]
	pmi_img.upload_file(other_path + pmi_name)

	# 1-6. HYG
	print("4. HYG")
	child_page.children.add_new(SubsubheaderBlock, title = 'HYG Stock')
	child_page.children.add_new(TextBlock, title = '부도 위험이 낮아질수록 가격이 오르는 주식상품')

	hyg_img = child_page.children.add_new(ImageBlock, width=500)
	hyg_img.upload_file(data_path + "HYG-1month.png")

	# 2. 경기
	child_page.children.add_new(HeaderBlock, title = '경기')
	child_page.children.add_new(TextBlock, title = ' ')

	# 2-1. S&P 500
	print("5. S&P 500")
	child_page.children.add_new(SubsubheaderBlock, title = 'S&P 500')

	snp_img = child_page.children.add_new(ImageBlock, width=500)
	snp = re.compile("^p0")
	snp_name = list(filter(snp.search, other_files))[0]
	snp_img.upload_file(other_path + snp_name)

	# 2-2. 장단기금리차
	v
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
	print("7. un-employment")
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
	print("8. others...")
	# 3-1. Fear & Greed Index
	child_page.children.add_new(SubsubheaderBlock, title = 'Fear & Greed Index')
	child_page.children.add_new(TextBlock, title = '40 이하: 시기상 저렴 & 공포')
	child_page.children.add_new(TextBlock, title = '40 <= x <= 60: 중립 ~ 매수 구간')
	child_page.children.add_new(TextBlock, title = '60 이상: 욕심 과열')

	fg_img = child_page.children.add_new(ImageBlock, width=800)
	fg_img.upload_file(other_path + "FG_image.png")

	print("UPLOADED! " + now_f)
