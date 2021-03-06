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
from notion.block import BookmarkBlock
import time

from tzlocal import get_localzone

import notion
def call_load_page_chunk(self, page_id):

    if self._client.in_transaction():
        self._pages_to_refresh.append(page_id)
        return

    data = {
        "pageId": page_id,
        "limit": 100,
        "cursor": {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False,
    }

    recordmap = self._client.post("loadPageChunk", data).json()["recordMap"]

    self.store_recordmap(recordmap)

def call_query_collection(
    self,
    collection_id,
    collection_view_id,
    search="",
    type="table",
    aggregate=[],
    aggregations=[],
    filter={},
    sort=[],
    calendar_by="",
    group_by="",
):

    assert not (
        aggregate and aggregations
    ), "Use only one of `aggregate` or `aggregations` (old vs new format)"

    # convert singletons into lists if needed
    if isinstance(aggregate, dict):
        aggregate = [aggregate]
    if isinstance(sort, dict):
        sort = [sort]

    data = {
        "collectionId": collection_id,
        "collectionViewId": collection_view_id,
        "loader": {
            "limit": 1000000,
            "loadContentCover": True,
            "searchQuery": search,
            "userLocale": "en",
            "userTimeZone": str(get_localzone()),
            "type": type,
        },
        "query": {
            "aggregate": aggregate,
            "aggregations": aggregations,
            "filter": filter,
            "sort": sort,
        },
    }

    response = self._client.post("queryCollection", data).json()

    self.store_recordmap(response["recordMap"])

    return response["result"]

def search_pages_with_parent(self, parent_id, search=""):
    data = {
        "query": search,
        "parentId": parent_id,
        "limit": 100,
        "spaceId": self.current_space.id,
    }
    response = self.post("searchPagesWithParent", data).json()
    self._store.store_recordmap(response["recordMap"])
    return response["results"]

notion.store.RecordStore.call_load_page_chunk = call_load_page_chunk
notion.store.RecordStore.call_query_collection = call_query_collection
notion.client.NotionClient.search_pages_with_parent = search_pages_with_parent

# main definition
if __name__ == "__main__":
	
	# get token
	niceguy_token = "0cc9bbdeea34ee61213d47d597353287eb114fec38aad86717fa0d4ac599bf044ce5ec07ac7f88daf06d3493657968d39441b9dcf6fb9d0f1d5d55c9d340997c93bffecc59123ee3384fa2d08fab"
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
	child_page.children.add_new(SubsubheaderBlock, title = 'PMI (기준: 50)')

	pmi_img = child_page.children.add_new(ImageBlock, width=500)    
	pmi = re.compile("^PMI")
	pmi_name = list(filter(pmi.search, other_files))[0]
	pmi_img.upload_file(other_path + pmi_name)

	# 1-6. HYG
	child_page.children.add_new(SubsubheaderBlock, title = 'HYG Stock')
	child_page.children.add_new(TextBlock, title = '부도 위험이 낮아질수록 가격이 오르는 주식상품')

	hyg_img = child_page.children.add_new(ImageBlock, width=500)
	hyg_img.upload_file(data_path + "HYG-1month.png")
	
	# 1-7. Libor
	libor_df = pd.read_csv(other_path + "usd_libor.csv", sep = ",")
	
	libor_df.columns = ['label', 'value']
	overnight_libor = str(round(float(libor_df.loc[libor_df.label == '1 week'].value), 4))
	week1_libor = str(round(float(libor_df.loc[libor_df.label == '1 week'].value), 4))
	month1_libor = str(round(float(libor_df.loc[libor_df.label == '1 week'].value), 4))
	month12_libor = str(round(float(libor_df.loc[libor_df.label == '1 week'].value), 4))
	
	child_page.children.add_new(HeaderBlock, title = '리보 금리')
	child_page.children.add_new(TextBlock, title = '영국 은행끼리 빌리는 돈(콜금리) 비슷')
	child_page.children.add_new(TextBlock, title = '단기 리보금리 > 장기 리보금리 일 경우 위험신호')
	child_page.children.add_new(TextBlock, title = ' ')
	
	child_page.children.add_new(TextBlock, title = '당일 리보금리')
	child_page.children.add_new(TextBlock, title = overnight_libor)
	child_page.children.add_new(TextBlock, title = '1주 리보금리')
	child_page.children.add_new(TextBlock, title = overnight_libor)
	child_page.children.add_new(TextBlock, title = '1달 리보금리')
	child_page.children.add_new(TextBlock, title = overnight_libor)
	child_page.children.add_new(TextBlock, title = '1년 리보금리')
	child_page.children.add_new(TextBlock, title = overnight_libor)
	
	# 1-8. 
	child_page.children.add_new(SubheaderBlock, title = "FOMC 일정")
	child_page.children.add_new(TextBlock, title = '긴급 컨퍼런스 콜 발생 시 위험신호')
	
	fomc_url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
	fomc_block = child_page.children.add_new(BookmarkBlock)
	fomc_block.set_new_link(fomc_url)
	
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
	
	# 2-37. Yieldcurve
	child_page.children.add_new(SubsubheaderBlock, title = 'Yield Curve')
	yield_img = child_page.children.add_new(ImageBlock, width=500)
	yield_img.upload_file(data_path + "yield_curve.png")
	
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
