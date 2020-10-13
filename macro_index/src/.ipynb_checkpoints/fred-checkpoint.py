#!/usr/bin/python

# load library
import requests
import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys

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


# main definition
if __name__ == "__main__":
	api_keys = ["08e04acc750c26678182a33fe90050b4", "2cf918e4dfe6d347d99e73e75930f4a3","752db7a401cae5103d2f5493abd8e5d7", "45a87a079750aca5f50296985543695d"]
	series_list = ["T10YIE", "T10Y2Y", "UNRATE", "FEDFUNDS", "USD12MD156N", "USD1WKD156N","BAMLH0A0HYM2", "TEDRATE"]
	
	api_key = api_keys[0]
	save_path = os.getcwd() + "/data"
	
	if not os.path.isdir(save_path):
		os.mkdir(save_path)
	
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