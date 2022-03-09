#!/usr/bin/python

# load library
import requests
import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
import sys
import re
from fear_greed_index import CNNFearAndGreedIndex
import fitz
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
from cairosvg import svg2png

# download file from url
def fredREQ(url, headers, param=None, retries=3):
	resp = None

	try:
		resp = requests.get(url, params=param, headers=headers)
		resp.raise_for_status()
	except requests.exceptions.HTTPError as e:
		if 500 <= resp.status_code < 600 and retries > 0:
			print('Retries : {0}'.format(retries))
			return fredREQ(url, param, retries - 1)
		else:
			return resp.status_code
	return resp


# make url
def fredURL(api_key, series):

	# make series url
	base_url = "https://api.stlouisfed.org/fred/series/observations?"
	query_key = "api_key=" + api_key
	query_file_type = "file_type=json"
	query_ob_end = datetime.now()
	query_ob_end_f = "observation_end=" + query_ob_end.strftime("%Y-%m-%d")
	query_ob_start = query_ob_end - relativedelta(years=2)
	query_ob_start_f = "observation_start=" + query_ob_start.strftime("%Y-%m-%d")
	series_id = "series_id=" + series

	query_list = [query_key, query_file_type, query_ob_start_f, query_ob_end_f, series_id]

	# series url
	series_url = base_url
	for query in query_list:
		series_url += "&" + query

	return series_url



# download file from url
def pdfDownload(save_path, url, headers, file_nm, param=None, retries=3):
	resp = None

	try:
		resp = requests.get(url, params=param, headers=headers)
		resp.raise_for_status()

		pdf_layer = save_path +  file_nm + ".pdf"

		with open(pdf_layer, 'wb') as f:
			f.write(resp.content)
		#print("complete writing pdf!")

	except requests.exceptions.HTTPError as e:
		if 500 <= resp.status_code < 600 and retries > 0:
			print('Retries : {0}'.format(retries))
			return getDownload(url, param, retries - 1)
		else:
			return resp.status_code
	return resp

# PDF imgage
def importImgFromPDF(save_path, file, start_page = 1, end_page = 1):

	doc = fitz.open(file)

	# get img page by
	for i in range( start_page-1, end_page ):
		for img in doc.getPageImageList(i):
			xref = img[0]
			pix = fitz.Pixmap(doc, xref)
			if pix.n < 5:  # this is GRAY or RGB
				pix.writePNG(save_path + "p%s-%s.png" % (i, xref))
			else:  # CMYK: convert to RGB first
				pix1 = fitz.Pixmap(fitz.csRGB, pix)
				pix1.writePNG(save_path + "p%s-%s.png" % (i, xref))
				pix1 = None
			pix = None

	#print("img from PDF has been saved!")

def importImgFromURL(save_path, url, file_nm):

	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	img_save_path = save_path + file_nm + '.png'
	img.save(img_save_path)
	#print("img from URL has been saved!")


# download file from url
def reqPage(url, headers, param=None, retries=3):
	resp = None

	try:
		resp = requests.get(url, params=param, headers=headers)
		resp.raise_for_status()
	except requests.exceptions.HTTPError as e:
		if 500 <= resp.status_code < 600 and retries > 0:
			print('Retries : {0}'.format(retries))
			return reqPage(url, param, retries - 1)
		else:
			return resp.status_code
	return resp

def getSoup(url):
	headers = {'Referer': url,
			   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

	req = reqPage(url, headers)
	req_txt = req.text
	soup = BeautifulSoup(req_txt, 'html.parser')
	
	return soup

def getYieldDf(soup):
	yield_chart = soup.find_all('table',{'class': 't-chart'})
	columns = yield_chart[0].find_all('th', {'scope' : 'col'})
	yield_cols = [x.text for x in columns]

	values = yield_chart[0].find_all('tr',{'class':['oddrow','evenrow']}) # two columns find

	yield_df = pd.DataFrame() # get yield data

	for val in values:

		vals = val.find_all('td', {'class':'text_view_data'})
		yield_vals = [x.text for x in vals]

		df = pd.DataFrame([yield_vals], columns = yield_cols)

		yield_df = pd.concat([yield_df, df], axis = 0)
        
	return yield_df


# main definition
if __name__ == "__main__":
	api_keys = ["08e04acc750c26678182a33fe90050b4", "2cf918e4dfe6d347d99e73e75930f4a3","752db7a401cae5103d2f5493abd8e5d7", "45a87a079750aca5f50296985543695d"]
    
	api_key = api_keys[0]
	save_path = os.getcwd() + "/data"

    # series list ticker
    # T10YIE - 10year break even rate, 10년 물가 상승률
    # T10Y2Y - 10 - 2, 장단기 금리차
    # UNRATE - 실업률
    # FEDFUNDS - 금리
    # USD1WKD156N, USD12MD156N - 리보금리
    # BAMLH0A0HYM2 - 부도위험
    # DGS10, DGS20 - 10, 20년 장기 금리
    
	series_list = ["T10YIE", # 부도위험
                   "BAMLH0A0HYM2", # 부도위험
                   "T10Y2Y", # 장단기 금리차
                   "FEDFUNDS"] # 금리
    
	if not os.path.isdir(save_path):
		os.mkdir(save_path)
	
    ############################################
    # 1. get series from fred
    ############################################
    
	# loop by series
	for series in series_list:
		# make url
		series_url = fredURL(api_key, series)
		
		# make header
		headers = {'Referer': series_url,
				   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

		# api key error exception
		try:
			series_request = fredREQ(series_url, headers)
		except:
			series_request = 500
			k = 1
			while isinstance(series_request, int) and k < len(api_keys):
				api_key_update = api_keys[k]
				series_url_update = fredURL(api_key_update, series)
				series_request = fredREQ(series_url_update, headers)
				k = k + 1

		if isinstance(series_request, int):
			continue;

		series_json = series_request.json()
		series_df = pd.json_normalize(series_json['observations'])

		series_result = series_df[['date', 'value']]
		
		layer = save_path + "/" + series + ".txt"

		series_result.to_csv(layer, sep="|", index = False)

    ############################################
    # 2. cnn fear and greed
    ############################################
	cnn_fg = CNNFearAndGreedIndex.CNNFearAndGreedIndex()
	idx_str = cnn_fg.get_index()
    
	idx_evaluate = re.findall(r'\(.*?\)',idx_str)
	idx_number = [int(s) for s in idx_str.split() if s.isdigit()]
    
	CNN_DF = pd.DataFrame(zip(idx_evaluate, idx_number), columns = ['idx','value'])
	layer = save_path + "/cnn_df.txt"

	CNN_DF.to_csv(layer, sep="|", index = False)
	
    
    ############################################
    # 3. S&P 500 12 FWD EPS
    ############################################
	today = datetime.now()

	last_friday = today + relativedelta(weekday=FR(-1))
	last_friday_str = last_friday.strftime("%m%d%y")

	pdf_url = "https://www.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_" + last_friday_str + "A.pdf"
	headers = {'Referer': pdf_url,
		   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
	save_name = "12fwd_" + last_friday_str
	
	pdfDownload(save_path, pdf_url, headers, save_name)

	file_logic = not os.path.isfile( save_path + save_name )
	
	i = 0
	while file_logic:
		i += 1
		last_friday = today + relativedelta(weekday=FR(-i))
		last_friday_str = last_friday.strftime("%m%d%y")

		pdf_url = "https://www.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_" + last_friday_str + ".pdf"
		headers = {'Referer': pdf_url,
			   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
		save_name = "12fwd_" + last_friday_str
		
		pdfDownload(save_path, pdf_url, headers, save_name)

		file_logic = not os.path.isfile( save_path + save_name + ".pdf" )

	pdf_which = save_path + save_name + ".pdf"
	importImgFromPDF(save_path, pdf_which, 1, 1)

	rm_file = save_path + "p0-12.png"
	#os.remove(pdf_which)
	os.remove(rm_file)
    
    ############################################
    # 4. Fidelity Business Cycle
    ############################################

	url = "https://institutional.fidelity.com/app/item/RD_13569_40890/business-cycle-update.html"
	soup = getSoup(url)
	imgs = soup.find_all('svg')
	svg2png(bytestring=imgs[3].encode('utf-8'),write_to= save_path + 'business_cycle.png')
    