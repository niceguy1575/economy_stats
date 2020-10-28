#!/usr/bin/python

# setup notion
import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import ImageBlock
from notion.block import HeaderBlock
from notion.block import SubheaderBlock
from notion.block import SubsubheaderBlock
from notion.block import PageBlock
from notion.block import BookmarkBlock
import time

# main definition
if __name__ == "__main__":

	# get token
	niceguy_token = "69c9a31ea3fd3455aa679a38be6b4ab92faee8ee049caf00875cbc25751e02738c74c243f7c6bffe60362b826a7a3ff847b2d1453b09d27ced4ea42ff8517efc97e7e14eed49c68c4a0e4b3a0aa1"
	client = NotionClient(token_v2 = niceguy_token)
	page = client.get_block("https://www.notion.so/niceguy1575/564d7bec3a784e6894731300389bfefc")

	now = datetime.now() + timedelta(days=1)
	now_f = now.strftime("%Y-%m-%d")
	page.children.add_new(PageBlock, title=now_f)

	# data load
	save_path = os.getcwd() + "/save/"
	url_path = os.getcwd() + ""
	##### page contents
	child_id = [c.id for c in page.children][-1]
	child_page = client.get_block(child_id)
	stocks = ['AAPL', 'GOOGL', 'MA', 'TSM', 'SBUX']

	stock_url1 = ['https://www.marketscreener.com/quote/stock/APPLE-INC-4849/company/',
			'https://www.marketscreener.com/quote/stock/ALPHABET-INC-24203373/company/',
			'https://www.marketscreener.com/quote/stock/TAIWAN-SEMICONDUCTOR-MANU-40246786/company/',
			'https://www.marketscreener.com/quote/stock/MASTERCARD-INCORPORATED-17163/company/',
'https://www.marketscreener.com/quote/stock/STARBUCKS-CORPORATION-4905/company/']
	stock_url2 = ['https://www.marketscreener.com/quote/stock/APPLE-INC-4849/financials/',
		'https://www.marketscreener.com/quote/stock/ALPHABET-INC-24203373/financials/',
		'https://www.marketscreener.com/quote/stock/MASTERCARD-INCORPORATED-17163/financials/',
		'https://www.marketscreener.com/quote/stock/TAIWAN-SEMICONDUCTOR-MANU-40246786/financials/',
'https://www.marketscreener.com/quote/stock/STARBUCKS-CORPORATION-4905/financials/']
	stock_url3 = ['https://www.marketbeat.com/stocks/NASDAQ/' + x + '/financials/' for x in stocks]

	stock_url_df = pd.DataFrame({'stock_name': stocks, 'url1': stock_url1, 'url2': stock_url2, 'url3': stock_url3})
	
	etfs = ['QQQ','IVV', 'SPY', 'VIG']

	etf_url1 = ['https://etfdb.com/etf/' + etf + '/#etf-ticker-profile' for etf in etfs]
	etf_url2 = ['https://www.etf.com/' + etf + '#overview' for etf in etfs]
	etf_url_df = pd.DataFrame({'etf_name': etfs, 'url1': etf_url1, 'url2': etf_url2})

	#### stock part
	for stock in stocks:
		print(stock)

		tbl_name = stock + '_stats.txt'
		
		# 1. read & paste stat_df
		stat_df = pd.read_csv(save_path + stock + "_stats.txt", sep = "|")
		stat_value = stat_df.stats.astype(str).values
		
		child_page.children.add_new(PageBlock, title=stock)

		grand_child_id = [c.id for c in child_page.children][-1]

		grand_child_page = client.get_block(grand_child_id)

		grand_child_page.children.add_new(HeaderBlock, title = stock + ' ' + now_f)
		
		grand_child_page.children.add_new(SubheaderBlock, title = "sector")
		grand_child_page.children.add_new(TextBlock, title = '섹터: ' + stat_value[0])
		
		grand_child_page.children.add_new(SubheaderBlock, title = "시가총액")
		
		market_cap = str(round(int(stat_value[1])/1e12, 4))
		
		grand_child_page.children.add_new(TextBlock, title = '시가총액: ' + market_cap + "(단위: 조$)")
		
		dividend = stat_value[2]
		grand_child_page.children.add_new(SubheaderBlock, title = "배당률")
		grand_child_page.children.add_new(TextBlock, title = '배당률: ' + dividend)
		
		per = str(round(float(stat_value[3]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "PER")
		grand_child_page.children.add_new(TextBlock, title = 'PER: ' + per)
		
		eps = str(round(float(stat_value[4]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "EPS")
		grand_child_page.children.add_new(TextBlock, title = 'EPS: ' + eps)
		
		roe = str(round(float(stat_value[6]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "ROE")
		grand_child_page.children.add_new(TextBlock, title = 'ROE: ' + roe)

		price = str(round(float(stat_value[5]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "Stock Price(종가)")
		grand_child_page.children.add_new(TextBlock, title = 'Stock Price: ' + price)
		
		target = str(round(float(stat_value[7]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "Target Price(적정주가)")
		grand_child_page.children.add_new(TextBlock, title = 'Target Price: ' + target)

		# 2. add image
		stock_image = grand_child_page.children.add_new(ImageBlock, width=650)
		stock_image.upload_file(save_path + stock + "_analysis.png")

		# 3. 유관 페이지 url
		url1 = stock_url_df.loc[stock_url_df.stock_name == stock].copy().url1.values[0]
		url2 = stock_url_df.loc[stock_url_df.stock_name == stock].copy().url2.values[0]
		url3 = stock_url_df.loc[stock_url_df.stock_name == stock].copy().url3.values[0]
		
		grand_child_page.children.add_new(SubheaderBlock, title = "MarketScreener - company")
		url1_block = grand_child_page.children.add_new(BookmarkBlock)
		url1_block.set_new_link(url1)

		grand_child_page.children.add_new(SubheaderBlock, title = "MarketScreener - financials")
		url2_block = grand_child_page.children.add_new(BookmarkBlock)
		url2_block.set_new_link(url2)

		grand_child_page.children.add_new(SubheaderBlock, title = "MarketBeat - financials")
		url3_block = grand_child_page.children.add_new(BookmarkBlock)
		url3_block.set_new_link(url3)
		
	print("STOCK UPLOADED! " + now_f)
	#### etf part
	for etf in etfs:
		print(etf)

		tbl_name = etf + '_stats.txt'
		
		# 1. read & paste stat_df
		stat_df = pd.read_csv(save_path + etf + "_stats.txt", sep = "|")
		stat_value = stat_df.stats.astype(str).values
		
		child_page.children.add_new(PageBlock, title=etf)

		grand_child_id = [c.id for c in child_page.children][-1]

		grand_child_page = client.get_block(grand_child_id)

		grand_child_page.children.add_new(HeaderBlock, title = etf + ' ' + now_f)
		
		price = str(round(float(stat_value[0]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "etf Price(종가)")
		grand_child_page.children.add_new(TextBlock, title = 'etf Price: ' + price)
		
		volume = str(round(float(stat_value[1]), 2) )
		grand_child_page.children.add_new(SubheaderBlock, title = "Volume (거래량)")
		grand_child_page.children.add_new(TextBlock, title = 'Volume: ' + volume)
		
		dividend = stat_value[2]
		grand_child_page.children.add_new(SubheaderBlock, title = "배당률")
		grand_child_page.children.add_new(TextBlock, title = '배당률: ' + dividend)
		
		# 2. add image
		etf_image = grand_child_page.children.add_new(ImageBlock, width=650)
		etf_image.upload_file(save_path + etf + "_analysis.png")

		# 3. 유관 페이지 url
		url1 = etf_url_df.loc[etf_url_df.etf_name == etf].copy().url1.values[0]
		url2 = etf_url_df.loc[etf_url_df.etf_name == etf].copy().url2.values[0]
		
		grand_child_page.children.add_new(SubheaderBlock, title = "MarketScreener - company")
		url1_block = grand_child_page.children.add_new(BookmarkBlock)
		url1_block.set_new_link(url1)

		grand_child_page.children.add_new(SubheaderBlock, title = "MarketScreener - financials")
		url2_block = grand_child_page.children.add_new(BookmarkBlock)
		url2_block.set_new_link(url2)
		
	print("ETF UPLOADED! " + now_f)
