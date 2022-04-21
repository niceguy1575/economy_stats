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


def requestURL(url, headers, requestType, data = None, retries=10):
	resp = None

	try:
		resp = requests.request(requestType, url, json = data, headers = headers)
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


def BlockHeader(url, requestType, headers, headingType, text = None):
	
	heading = 'heading_1' if headingType == 1 else 'heading_2' if headingType == 2 else 'heading_3'
	
	data = {
	"children": [ {
		  "type": heading,
		  heading: {
			"rich_text": [{
			  "type": "text",
			  "text": {
				"content": text,
			  }
			}],
			"color": "default"
		  }
	} ] }
	
	return requestURL(url, headers, requestType, data)

def BlockParagraph(url, requestType, headers, text = None):
		
	data = {
	"children": [ {
		  "type": "paragraph",
		  "paragraph": {
			"rich_text": [{
			  "type": "text",
			  "text": {
				"content": text
			  }
			}]
		  } 
		} ] }
	
	return requestURL(url, headers, requestType, data)

def BlockEmbed(url, requestType, headers, embedURL):
		
	data = {
	"children": [ {
			  "type": "embed",
				"embed": {
					"url": embedURL
			  }
	} ] }
	
	return requestURL(url, headers, requestType, data)

def BlockBookmark(url, requestType, headers, bookmarkURL):
		
	data = {
	"children": [ {
			  "type": "bookmark",
				"bookmark": {
					"url": bookmarkURL
			  }
	} ] }
	
	return requestURL(url, headers, requestType, data)

if __name__ == "__main__":
	
	save_path = "/home/ec2-user/economyAlert/data"
	log_path = "/home/ec2-user/economyAlert/log"
	today = datetime.today()
	today_str = str(today.strftime("%Y-%m-%d"))
    
	log_message1 = '4. upload'
	os.system( 'echo "' + log_message1 + '" >> ' + log_path + '/economy_alert_log.txt' )
    
	# 0. 필요 데이터 setup
	now = datetime.now()
	now_f = now.strftime("%Y-%m-%d")

	notion_secret_key = ""
	target_page_id = "07cae222-fb62-4bc5-b402-e96c1c86ed70"
	
	data_dir = os.getcwd() + "/data/"
	files = os.listdir(data_dir)

	# url list
	ice_url = 'https://plotly.com/~niceguy1575/77/'
	fed_funds_url = 'https://plotly.com/~niceguy1575/81/'
	t10yt2_url = 'https://plotly.com/~niceguy1575/79/'
	inflate_url = 'https://plotly.com/~niceguy1575/75/'
	fomc_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
	fng_url = 'https://money.cnn.com/data/fear-and-greed'
	roro_url = 'https://www.mvis-indices.com/indices/customised/atac-risk-on-risk-off-domestic'

	log_message2 = '4-1. setup'
	os.system( 'echo "' + log_message2 + '" >> ' + log_path + '/economy_alert_log.txt' )

	# 1. 사전에 notion에서 사전에 페이지 획득 필요!
	post_url = "https://api.notion.com/v1/pages"
	headers = {
		"Accept": "application/json",
		"Notion-Version": "2022-02-22",
		"Content-Type": "application/json",
		"Authorization": "Bearer " + notion_secret_key
	}
	page_data = {
	"parent": { "page_id": target_page_id },
	"properties": {
		"title": {
			"title": [{ "type": "text", "text": { "content": now_f + ' 경제 리포트'} }]
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
	requestURL(post_url, headers, "POST", data = page_data)
	time.sleep(5)
    
	log_message3 = '4-2. create page'
	os.system( 'echo "' + log_message3 + '" >> ' + log_path + '/economy_alert_log.txt' )

	####################|################
	# child block 생성
	####################################
	# 새로 만들어진 page id 확인
	get_url = "https://api.notion.com/v1/blocks/"  + target_page_id +  "/children?page_size=100"

	id_request = requestURL(get_url, headers, "GET")
	parent_parse = pd.json_normalize(id_request.json())['results']
	children_df = pd.json_normalize(parent_parse[0])
	makingIDSeries = children_df[children_df.has_children == True].tail(n=1).id
	makingID = makingIDSeries.values[0]

	# 0. mailing list
	idstr = makingID.replace("-", "") 
	base_link = 'https://niceguy1575.notion.site/'
	mail_link = base_link + today_str + '-' + idstr
	
	pd.DataFrame([mail_link]).to_csv(save_path + '/' + 'mail_link.txt', sep = '|', index = False)

	log_message4 = '4-3. get child id'
	os.system( 'echo "' + log_message4 + '" >> ' + log_path + '/economy_alert_log.txt' )    

	####################################
	# notion api upload
	####################################
	childrenURL = 'https://api.notion.com/v1/blocks/' + makingID + '/children'
   
	BlockHeader(childrenURL, "PATCH", headers, headingType = 1, text ='중요 거시경제 지표 확인')

	# 1. 부도위험
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text ='부도위험 (ICE)')
	BlockParagraph(childrenURL, "PATCH", headers, text = 'target-index: 5')
	BlockEmbed(childrenURL, "PATCH", headers, embedURL = ice_url)
	log_message = '4-4. notion upload 1'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 2. 물가 상승률
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text ='물가상승률 (10년)')
	BlockParagraph(childrenURL, "PATCH", headers, text = 'target-inflation: 2%')
	BlockEmbed(childrenURL, "PATCH", headers, embedURL = inflate_url)
	log_message = '4-4. notion upload 2'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 3. fed 금리
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text ='금리')
	BlockEmbed(childrenURL, "PATCH", headers, embedURL = fed_funds_url)
	log_message = '4-4. notion upload 3'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 4. 장단기 금리차
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text ='장단기 금리차 (10년-2년)')
	BlockParagraph(childrenURL, "PATCH", headers, text = 'target-index: 0')
	BlockEmbed(childrenURL, "PATCH", headers, embedURL = t10yt2_url)
	log_message = '4-4. notion upload 4'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	BlockParagraph(childrenURL, "PATCH", headers, text = ' ')
	BlockHeader(childrenURL, "PATCH", headers, headingType = 1, text ='투자 참고 지표')

	# 5. FOMC 일정
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text ='FOMC 일정')
	BlockBookmark(childrenURL, "PATCH", headers, bookmarkURL = fomc_url)
	log_message = '4-4. notion upload 5'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 6. Fear & Greed index
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text = 'Fear & Greed Index')
	BlockParagraph(childrenURL, "PATCH", headers, text = '40 이하: 시기상 저렴 & 공포')
	BlockParagraph(childrenURL, "PATCH", headers, text = '40 ~ 60: 중립 ~ 매수 구간')
	BlockParagraph(childrenURL, "PATCH", headers, text = '60 이상: 욕심 과열')
	
	BlockBookmark(childrenURL, "PATCH", headers, bookmarkURL = fng_url)
	log_message = '4-4. notion upload 6'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 7. Risk on, Risk Off (roro 지수)
	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text = 'Risk on, Risk Off (roro 지수)')
	BlockParagraph(childrenURL, "PATCH", headers, text = '클수록 위험, 작을수록 공포')
	BlockBookmark(childrenURL, "PATCH", headers, bookmarkURL = roro_url)
	log_message = '4-4. notion upload 7'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    

	# 8. SnP 500 12 FWD EPS
	# pdf는 자주 바뀌지 않아, 오류가나도 page는 생성될 수 있도록 reading을 가장 마지막에 한다.
	txt_regex = re.compile('pdf.txt$')
	pdf_file = list(filter(txt_regex.search, files))
	pdf_link = pd.read_csv(data_dir + pdf_file[0], sep = "|")
	pdf_url = pdf_link['0'][0]

	BlockHeader(childrenURL, "PATCH", headers, headingType = 2, text = 'SnP 500 12 FWD EPS')
	BlockEmbed(childrenURL, "PATCH", headers, embedURL = pdf_url)
	log_message = '4-4. notion upload 8'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )    
    
	# 9. print etc...
	print("upload to notion! " + now_f)
    
	
	log_message = '4. upload success'
	os.system( 'echo "' + log_message + '" >> ' + log_path + '/economy_alert_log.txt' )