#!/usr/bin/python

# setup notion
import os
import pandas as pd
from datetime import datetime
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

# get token
niceguy_token = "c7570b064a2992f27adbf7b2b2e9f32846fdfeede4642ec922baa1a0567725644e4d2832f157083106779a1d9b30bc1382ec35130af276da8a302cb5892d09dc14ff97a2f36d31ead1168a85c22d"
client = NotionClient(token_v2 = niceguy_token)
page = client.get_block("https://www.notion.so/niceguy1575/07cae222fb624bc5b402e96c1c86ed70")

now = datetime.now()
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
# 1. 부도위험
child_page.children.add_new(HeaderBlock, title = '부도위험')
child_page.children.add_new(TextBlock, title = ' ')

child_page.children.add_new(SubheaderBlock, title = 'ICE')
# 1-1. ice
ice_value = data.loc[data.label == 'ice'].stat.astype(str).values

child_page.children.add_new(TextBlock, title = '부도위험 최신값: ' + ice_value[0])
child_page.children.add_new(TextBlock, title = '부도위험 전월대비 증가율: ' + ice_value[1] + "%")
child_page.children.add_new(TextBlock, title = '부도위험 전분기대비 증가율: ' + ice_value[2] + "%")
child_page.children.add_new(TextBlock, title = '부도위험 전년대비 증가율: ' + ice_value[2] + "%")

# 1-2. ice graph
child_page.children.add_new(SubsubheaderBlock, title = '부도위험 3month')

ice_img = child_page.children.add_new(ImageBlock, width=500)
ice_img.upload_file(data_path + "ICE.png")

#1-3. ted
child_page.children.add_new(SubheaderBlock, title = 'TED')

ted_value = data.loc[data.label == 'ted'].stat.astype(str).values

child_page.children.add_new(TextBlock, title = 'TED RATE 최신값: ' + ted_value[0])
child_page.children.add_new(TextBlock, title = 'TED RATE 전월대비 증가율: ' + ted_value[1] + "%")
child_page.children.add_new(TextBlock, title = 'TED RATE 전분기대비 증가율: ' + ted_value[2] + "%")

# 1-4. ted graph
child_page.children.add_new(SubsubheaderBlock, title = 'TED RATE 6month')

ted_img = child_page.children.add_new(ImageBlock, width=500)
ted_img.upload_file(data_path + "TED.png")

# 1-5. PMI
child_page.children.add_new(SubsubheaderBlock, title = 'PMI (기준: 50)')

pmi_img = child_page.children.add_new(ImageBlock, width=500)    
pmi = re.compile("^PMI")
pmi_name = list(filter(pmi.search, other_files))[0]
pmi_img.upload_file(other_path + pmi_name)

# 2. 경기
child_page.children.add_new(HeaderBlock, title = '경기')
child_page.children.add_new(TextBlock, title = ' ')

# 2-1. S&P 500
child_page.children.add_new(SubsubheaderBlock, title = 'S&P 500')

snp_img = child_page.children.add_new(ImageBlock, width=500)
snp = re.compile("^p0")
snp_name = list(filter(snp.search, other_files))[0]
snp_img.upload_file(other_path + snp_name)

# 2-2. 장단기금리차
child_page.children.add_new(SubheaderBlock, title = '장단기 금리차')

t102y = data.loc[data.label == 'ls'].stat.astype(str).values

child_page.children.add_new(TextBlock, title = '장단기금리차 최신값: ' + t102y[0])
child_page.children.add_new(TextBlock, title = '장단기금리차 전월대비 증가율: ' + t102y[1] + "%")
child_page.children.add_new(TextBlock, title = '장단기금리차 전분기대비 증가율: ' + t102y[2] + "%")

# 2-3. 장단기 금리차 
child_page.children.add_new(SubsubheaderBlock, title = '장단기 금리차 6개월')

t102y_img = child_page.children.add_new(ImageBlock, width=500)
t102y_img.upload_file(data_path + "LS.png")

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

print("UPLOADED! " + now_f)