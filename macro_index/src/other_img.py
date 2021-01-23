#!/usr/bin/python

# load library
import requests
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
import fitz
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time

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


# main definition
if __name__ == "__main__":

	# 0. save_path
	save_path = os.getcwd() + "/data/"

	if os.path.isdir(save_path)  is not True:
		os.mkdir(save_path)
	
	# 1. get PMI image
	url = "https://tradingeconomics.com/united-states/business-confidence"
	headers = {'Referer': url,
			   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

	req = fredREQ(url, headers)
	req_txt = req.text
	soup = BeautifulSoup(req_txt, 'html.parser')

	imgs = soup.find_all('img')
	img_url = imgs[0]['src']

	today = datetime.now()

	pmi_nm = "PMI_image" #+ today_str
	importImgFromURL(save_path, img_url, pmi_nm)

	# 2. S&P500 image    
	last_friday = datetime.now() + relativedelta(weekday=FR(-1))
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
		last_friday = datetime.now() + relativedelta(weekday=FR(-i))
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
	os.remove(pdf_which)
	os.remove(rm_file)
	
	# 3. Fear & Greed
	url = "https://money.cnn.com/data/fear-and-greed/"
	headers = {'Referer': url,
			   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

	req = fredREQ(url, headers)
	req_txt = req.text
	soup = BeautifulSoup(req_txt, 'html.parser')

	id_url = soup.find_all("div", {"id": "needleChart"})

	style_url = id_url[0]['style']
	img_url = style_url.split("('", 1)[1].split("')")[0]

	fear_greed_nm = "FG_image" #+ today_str
	importImgFromURL(save_path, img_url, fear_greed_nm)
