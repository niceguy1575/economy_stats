#!/usr/bin/python

import requests
import yfinance as yf
from bs4 import BeautifulSoup
import re
import numpy as np
from datetime import datetime, timedelta
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
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()

    data = yf.download(stock_name, start_date, end_date)

    x = data.index.astype(str)
    y1 = np.log(data.Close)
    y2 = data.Volume / 100000000

    ax1.plot(x, y1, 'g-')
    ax2.bar(x, y2)

    tick1 = np.append(ax1.get_xticks()[::10], len(x))
    tick2 = np.append(ax2.get_xticks()[::10], len(x))

    ax1.set_xticks(tick1)
    ax2.set_xticks(tick2)

    fig.suptitle(stock_name + ' Chart', fontsize = 20)
    fig.autofmt_xdate(rotation=45)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Growth[=log(stock price)]', color='g', fontsize = 12)
    ax2.set_ylabel('Stock trade volume[Volume], 100 million', color='b', fontsize = 12)    
    
    fig.savefig(save_path + save_name)


def get_stats_stock(stock_name, save_path, tbl_name, plot_name):
		##### 1. get statistics
	stock_ticker = yf.Ticker(stock_name)

	stock_info = stock_ticker.info

	# sector
	# 시가총액: marketCap; 	# 배당률: dividendRatel;	# pe ratio: trailingPE;	# eps: trailingEps;

	sector = stock_info['sector']
	beta = stock_info['beta']
	cap = stock_info['marketCap']
	dividends = stock_info['dividendRate']
	per = stock_info['trailingPE']
	eps = stock_info['trailingEps']
	close_price = stock_info['previousClose']

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
    
	roe_text = roe[0].text
    
	if roe_text == "N/A":
		roe_num = 0
	else:
		roe_num = float(re.sub('%', '', roe_text))

	target_price = eps * roe_num
	
	stats = [sector, cap, dividends, beta, per, eps, close_price, roe_num, target_price]
	lis = ['sector', '시가총액', '배당률', 'beta','PER', 'EPS', '종가', 'ROE', '적정주가']

	stat_df = pd.DataFrame({'label': lis, 'stats': stats})
	stat_df.to_csv( save_path + tbl_name, sep = "|", index = False)
	########## do analyze chart data

	# draw stock price
	end_date = datetime.now() + timedelta(days = 1)
	end_str = end_date.strftime('%Y-%m-%d')

	start_date = end_date - relativedelta(months=3)
	start_str = start_date.strftime('%Y-%m-%d')

	draw_analysis_plot(stock_name, start_str, end_str, save_path, plot_name)

def get_stats_etf(stock_name, save_path, tbl_name, plot_name):
	##### 1. get statistics
	etf_ticker = yf.Ticker(stock_name)

	etf_info = etf_ticker.info

	close_price = etf_info['previousClose']
	volume = etf_info['volume']
	dividends = etf_info['dividendRate']
	beta = etf_info['beta3Year']

	stats = [close_price, volume, dividends, beta]
	lis = ['종가', '거래량', '배당률', 'beta']

	stat_df = pd.DataFrame({'label': lis, 'stats': stats})
	stat_df.to_csv( save_path + tbl_name, sep = "|", index = False)

	# draw stock price
	end_date = datetime.now() + timedelta(days = 1)
	end_str = end_date.strftime('%Y-%m-%d')

	start_date = end_date - relativedelta(months=3)
	start_str = start_date.strftime('%Y-%m-%d')

	draw_analysis_plot(stock_name, start_str, end_str, save_path, plot_name)

# main definition
if __name__ == "__main__":

	save_path = os.getcwd() + "/save/"

	if os.path.isdir(save_path)  is not True:
			os.mkdir(save_path)
	
	### STOCK
	stocks = ['AAPL', 'TSM']

	for stock in stocks:
		print(stock)
		plot_name = stock + '_analysis'
		tbl_name = stock + '_stats.txt'

		get_stats_stock(stock, save_path, tbl_name, plot_name)
	
	### ETF
	etfs = ['QQQ', 'SPY', 'SKYY']
	for etf in etfs:
		print(etf)
		plot_name = etf + '_analysis'
		tbl_name = etf + '_stats.txt'

		get_stats_etf(etf, save_path, tbl_name, plot_name)
