#!/usr/bin/python

# setup notion
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
	niceguy_token = "69c9a31ea3fd3455aa679a38be6b4ab92faee8ee049caf00875cbc25751e02738c74c243f7c6bffe60362b826a7a3ff847b2d1453b09d27ced4ea42ff8517efc97e7e14eed49c68c4a0e4b3a0aa1"
	client = NotionClient(token_v2 = niceguy_token)
	page = client.get_block("https://www.notion.so/niceguy1575/564d7bec3a784e6894731300389bfefc")

	now = datetime.now()
	now_f = now.strftime("%Y-%m-%d")
	page.children.add_new(PageBlock, title=now_f)

	# data load
	save_path = os.getcwd() + "/save/"
	time.sleep(5)
	
	##### page contents
	child_id = [c.id for c in page.children][-1]

	child_page = client.get_block(child_id)

	stocks = ['AAPL', 'GOOGL', 'MA', 'TSM']

	# page insert start...
	for stock in stocks:
		print(stock)
		
		tbl_name = stock + '_stats.txt'
		
		# 1. read & paste stat_df
		stat_df = pd.read_csv(save_path + stock + "_stats.txt", sep = "|")
		stat_value = stat_df.stats.astype(str).values
		child_page.children.add_new(HeaderBlock, title = stock + ' ' + now_f)
		
		child_page.children.add_new(SubheaderBlock, title = "sector")
		child_page.children.add_new(TextBlock, title = '섹터: ' + stat_value[0])
		
		child_page.children.add_new(SubheaderBlock, title = "시가총액")
		
		market_cap = str(round(int(stat_value[1])/100000000, 1))
		
		child_page.children.add_new(TextBlock, title = '시가총액: ' + market_cap + "(단위: 억$)")
		
		child_page.children.add_new(SubheaderBlock, title = "배당률")
		child_page.children.add_new(TextBlock, title = '배당률: ' + stat_value[2])
		
		child_page.children.add_new(SubheaderBlock, title = "PER")
		child_page.children.add_new(TextBlock, title = 'PER: ' + stat_value[3])
		
		child_page.children.add_new(SubheaderBlock, title = "EPS")
		child_page.children.add_new(TextBlock, title = 'EPS: ' + stat_value[4])
		
		child_page.children.add_new(SubheaderBlock, title = "Stock Price(종가)")
		child_page.children.add_new(TextBlock, title = 'Stock Price: ' + stat_value[5])
		
		child_page.children.add_new(SubheaderBlock, title = "Target Price(적정주가)")
		child_page.children.add_new(TextBlock, title = 'Target Price: ' + stat_value[6])

		# 2. add image
		stock_image = child_page.children.add_new(ImageBlock, width=650)
		stock_image.upload_file(save_path + stock + "_analysis.png")
		
	print("UPLOADED! " + now_f)