#!/usr/bin/python

import requests
import yfinance as yf
from bs4 import BeautifulSoup
import re
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

# download file from url
def pageRequest(url, headers, param=None, retries=3):
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

def draw_analysis_plot(stock_name, start_date, end_date,
						save_path, save_name):

    fig, ax1 = plt.subplots()
    plt.suptitle('ggplot style')
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()

    data = yf.download(stock_name, start_date, end_date)

    x = data.index
    y1 = np.log(data.Close)
    y2 = data.Volume

    ax1.plot(x, y1, 'g-')
    ax2.bar(x, y2)

    fig.suptitle(stock_name + ' Chart', fontsize = 20)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Growth[=log(stock price)]', color='g', fontsize = 12)
    ax2.set_ylabel('Stock trade volume[Volume]', color='b', fontsize = 12)
    
    fig.savefig(save_path + save_name)

def get_stats(stock_name, save_path, tbl_name, plot_name):
		##### 1. get statistics
	aapl = yf.Ticker(stock_name)

	aapl_info = aapl.info

	# sector
	# 시가총액: marketCap; 	# 배당률: dividendRatel;	# pe ratio: trailingPE;	# eps: trailingEps;

	sector = aapl_info['sector']
	cap = aapl_info['marketCap']
	dividends = aapl_info['dividendRate']
	per = aapl_info['trailingPE']
	eps = aapl_info['trailingEps']
	close_price = aapl_info['previousClose']

	# ROE = Net Income / Shareholder Equity
	# BPS * ROE = EPS
	# 슈퍼개미 김정환식 적정주가 계산
	# (영업이익 또는 당기순이익) * (ROE*100) = 시가총액
	# EPS * (ROE*100) = 적정주가
	url = "https://finance.yahoo.com/quote/" + stock_name + "/key-statistics?p=" + stock_name
	headers = {'Referer': url,
	   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

	req = pageRequest(url, headers)

	req_txt = req.text
	soup = BeautifulSoup(req_txt, 'html.parser')

	span = soup.find_all("span")

	span_txt = [x.text for x in span]
	span_index = span_txt.index('Return on Equity')
	span_str = str(span[span_index])

	react_id = span_str.split("=")[1].split(">")[0]
	react_num = int(re.sub('"', '', react_id))

	target_num = react_num + 4

	roe = soup.find_all("td", {'data-reactid': target_num})
	roe_num = float(re.sub('%', '', roe[0].text))

	target_price = eps * roe_num
	
	stats = [sector, cap, dividends, per, eps, close_price, roe_num, target_price]
	lis = ['sector', '시가총액', '배당률', 'PER', 'EPS', '종가', 'ROE', '적정주가']

	stat_df = pd.DataFrame({'label': lis, 'stats': stats})
	stat_df.to_csv( save_path + tbl_name, sep = "|", index = False)
	print("1. stat")

	########## do analyze chart data

	# draw stock price
	end_date = datetime.now()
	end_str = end_date.strftime('%Y-%m-%d')

	start_date = end_date - relativedelta(months=3)
	start_str = start_date.strftime('%Y-%m-%d')

	draw_analysis_plot(stock_name, start_str, end_str, save_path, plot_name)

	print("2. plot")


# main definition
if __name__ == "__main__":

	save_path = os.getcwd() + "/save/"

	if os.path.isdir(save_path)  is not True:
			os.mkdir(save_path)

	stocks = ['AAPL', 'GOOGL', 'MA', 'TSM']

	for stock in stocks:
		print(stock)
		plot_name = stock + '_analysis'
		tbl_name = stock + '_stats.txt'

		get_stats(stock, save_path, tbl_name, plot_name)