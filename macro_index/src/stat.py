#!/usr/bin/python

# load data
import os
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf   

def economy_line_plot(data, month, standard, title, xlab, ylab, save_path, save_name):
	fig = plt.figure()
	plt.suptitle('ggplot style')
	
	newest_date =  data.date.tail(n=1).copy().values[0]
	newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()
	
	three_month = newest_datetime - relativedelta(months = month)
	three_month_f = three_month.strftime("%Y-%m-%d")

	try:
		three_month_data = data.loc[np.where(data.date == three_month_f)[0][0]:,:].copy()
	except:
		three_month_data = data.tail(n = month*30).copy()

	three_month_data.date =  pd.to_datetime(three_month_data.date, format='%Y-%m-%d')

	plt.plot(three_month_data.date, three_month_data.value)
	plt.axhline(y = standard, color = 'r')

	fig.suptitle(title, fontsize = 20)
	plt.xlabel(xlab, fontsize = 16)
	plt.ylabel(ylab, fontsize = 16)

	fig.savefig(save_path + save_name)
	
def get_newest_stat(data):
	newest_value = data.value.tail(n=1).copy().values[0]
	
	return newest_value

def last_value_stat(data, month):
	newest_date =  data.date.tail(n=1).copy().values[0]
	newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()
	newest_value = data.value.tail(n=1).copy().values[0]

	# last month
	last_month = newest_datetime - relativedelta(months = month)
	last_month_f = last_month.strftime("%Y-%m-%d")

	try: 
		last_month_value = data.loc[data.date == last_month_f,:].copy().value.values[0]
	except:
		last_month_value = data.tail(n = month*30).copy().value.values[0]

	stat1 = (newest_value - last_month_value) / last_month_value
	
	return round(stat1,2)

def draw_yh_stock_price(stock_name, start_date, end_date,
						save_path, save_name):

	fig = plt.figure()
	plt.suptitle('ggplot style')

	data = yf.download(stock_name, start_date, end_date) 

	plt.plot(data.index, data.Close)

	fig.suptitle("HYG 1month", fontsize = 20)
	plt.xlabel("Date", fontsize = 16)
	plt.ylabel("Stock Price", fontsize = 16)
	fig.savefig(save_path + save_name)

def draw_plot_two_axis(data1, data2, month,
					   save_path, save_name):
	
	# data type change
	data1.value = data1.value.replace(".", None)
	data1 = data1.loc[data1.value != ".",:].copy()
	data1.value = data1.value.astype(float)
	
	data2.value = data2.value.replace(".", None)
	data2 = data2.loc[data2.value != ".",:].copy()
	data2.value = data2.value.astype(float)
	
	# data 1
	newest_date =  data1.date.tail(n=1).copy().values[0]
	newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()

	three_month1 = newest_datetime - relativedelta(months = 1)
	three_month_f1 = three_month1.strftime("%Y-%m-%d")

	try:
		three_month_data1 = data1.loc[np.where(data1.date == three_month_f1)[0][0]:,:].copy()
	except:
		three_month_data1 = data1.tail(n = month*30).copy()

	three_month_data1.date =  pd.to_datetime(three_month_data1.date, format='%Y-%m-%d')

	# data 2
	newest_date =  data2.date.tail(n=1).copy().values[0]
	newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()

	three_month2 = newest_datetime - relativedelta(months = 1)
	three_month_f2 = three_month2.strftime("%Y-%m-%d")

	try:
		three_month_data2 = data2.loc[np.where(data2.date == three_month_f2)[0][0]:,:].copy()
	except:
		three_month_data2 = data2.tail(n = month*30).copy()

	three_month_data2.date =  pd.to_datetime(three_month_data2.date, format='%Y-%m-%d')
	
	########## figure

	fig, ax1 = plt.subplots()
	plt.xticks(rotation=45)

	ax2 = ax1.twinx()

	x = three_month_data1.date.astype(str)
	y1 = three_month_data1.value
	y2 = three_month_data2.value

	ax1.plot(x, y1, 'g-')
	ax2.plot(x, y2)

	fig.suptitle('10 & 20 maturity rate {} month'.format(1), fontsize = 20)
	fig.autofmt_xdate(rotation=45)

	ax1.set_xlabel('Date')
	ax1.set_ylabel('10 year', color='g', fontsize = 12)
	ax2.set_ylabel('20 year', color='b', fontsize = 12) 
	
	fig.savefig(save_path + save_name)
	
def getYieldSmry(date, date_type):
    
    if date_type == "today":
        yield_date_df = yield_df.loc[yield_date_series == date]
    
    elif date_type == 'week':
        yield_date_df = yield_df.loc[
            (yield_date_series.apply(lambda x: x.year) == date.year) &
            (yield_date_series.apply(lambda x: x.week) == date.week)
        ]
        
    elif date_type == 'month':
        yield_date_df = yield_df.loc[
            (yield_date_series.apply(lambda x: x.year) == date.year) &
            (yield_date_series.apply(lambda x: x.month) == date.month)
        ]
    else :
        return None

    yield_smry = yield_date_df.loc[:, yield_date_df.columns!='Date'].apply(lambda x: 
                                                      sum(x.apply(float)) / len(x.apply(float))
                                                      , axis = 'index')
    yield_smry_df = pd.DataFrame(yield_smry, columns = ['yield'])
    
    return yield_smry_df

# main definition
if __name__ == "__main__":
	#plt.rc('font', family='DejaVu')
	data_dir = os.getcwd() + "/data/"
	files = os.listdir(data_dir)

	txt_regex = re.compile('.txt$')

	txt_file = list(filter(txt_regex.search, files))

	save_path = os.getcwd() + "/plot/"
	if os.path.isdir(save_path)  is not True:
		os.mkdir(save_path)
	
	# text file
	for txt in txt_file:
		file = data_dir + txt
		data = pd.read_csv(file, sep = "|")

		# data type change
		data.value = data.value.replace(".", None)
		data = data.loc[data.value != ".",:].copy()
		data.value = data.value.astype(float)
		
		# 파일별 콘텐츠 생산
		if txt == "BAMLH0A0HYM2.txt": # ICE
			
			ice_stat1 = get_newest_stat(data)
			ice_stat2 = last_value_stat(data, month = 1)
			ice_stat3 = last_value_stat(data, month = 3)
			ice_stat4 = last_value_stat(data, month = 12)

			# figure
			economy_line_plot(data, month = 3, standard = 5,
							title = "ICE-3month", xlab = "date", ylab = "value",
							save_path = save_path,
							save_name = "ICE")
		elif txt == "TEDRATE.txt":
			ted_stat1 = get_newest_stat(data)
			ted_stat2 = last_value_stat(data, month = 1)
			ted_stat3 = last_value_stat(data, month = 3)
			
			economy_line_plot(data, month = 6, standard = 1,
					title = "TED-6month", xlab = "date", ylab = "value",
					save_path = save_path,
					save_name = "TED")
			
		elif txt == "T10Y2Y.txt":
			ls_stat1 = get_newest_stat(data)
			ls_stat2 = last_value_stat(data, month = 1)
			ls_stat3 = last_value_stat(data, month = 3)
			
			economy_line_plot(data, month = 6, standard = 0,
					 title = "LS-6month", xlab = "date", ylab = "value",
					 save_path = save_path,
					 save_name = "LS")
		elif txt == "FEDFUNDS.txt":
			fund_stat1 = get_newest_stat(data)
			fund_stat2 = last_value_stat(data, month = 1)
			
			economy_line_plot(data, month = 12, standard = 0,
					 title = "funds-1year", xlab = "date", ylab = "value",
					 save_path = save_path,
					 save_name = "funds_rate")
		elif txt == "UNRATE.txt":
			ur_stat1 = get_newest_stat(data)
			ur_stat2 = last_value_stat(data, month = 2)
			
			economy_line_plot(data, month = 6, standard = 0,
					 title = "unrate-6month", xlab = "date", ylab = "value",
					 save_path = save_path,
					 save_name = "unrate")			
		elif txt == "T10YIE.txt":
			economy_line_plot(data, month = 1, standard = 2,
					 title = "price-1month", xlab = "date", ylab = "value",
					 save_path = save_path,
					 save_name = "price")
		else:
			print("nothing to do on {}".format(txt))
	
	# draw maturity plot
	data1 = pd.read_csv(data_dir + "DGS10.txt", sep = "|")
	data.columns = ['date', 'value10']
	data2 = pd.read_csv(data_dir + "DGS20.txt", sep = "|")
	data.columns = ['date', 'value20']

	# 적은쪽에 맞추기
	data_tmp = pd.merge(data1, data2, on = 'date', how = 'inner')
	data1 = data_tmp[['date','value10']].copy()
	data2 = data_tmp[['date','value20']].copy()

	draw_plot_two_axis(data1, data2, 1, save_path = save_path, save_name = "long_maturity-1month")

	# draw stock price
	end_date = datetime.now()
	end_str = end_date.strftime('%Y-%m-%d')

	start_date = end_date - relativedelta(months=1)
	start_str = start_date.strftime('%Y-%m-%d')
	
	draw_yh_stock_price('HYG', start_str, end_str, save_path, "HYG-1month")
	
	# draw yield curve
	yield_df = pd.read_csv(data_dir + "yield_curve.csv", sep = ",")
	yield_date_series = yield_df.Date.apply(lambda x: datetime.strptime(x, '%m/%d/%y'))

	yield_today = yield_date_series.tail(n = 1).tolist()[0]

	yield_3m_before_day = (yield_today - relativedelta(months = 3))
	yield_1m_before_day = (yield_today - relativedelta(months = 1))
	yield_1w_before_day = (yield_today - relativedelta(weeks = 1))

	y_today = getYieldSmry(yield_today, date_type = 'today')
	y_1m = getYieldSmry(yield_1m_before_day, date_type = 'month')
	y_3m = getYieldSmry(yield_3m_before_day, date_type = 'month')
	y_1w = getYieldSmry(yield_1w_before_day, date_type = 'week')

	y_plt_data = pd.concat([y_today, y_1m, y_3m, y_1w], axis = 1)

	y_plt_data.columns = ['today: ' + yield_today.strftime('%Y-%m-%d'),
	'1mon_before: ' + yield_1m_before_day.strftime('%Y-%m'),
	'3mon_before: ' + yield_3m_before_day.strftime('%Y-%m'),
	'1week_before: ' + yield_1w_before_day.strftime('%Y-%w') + 'week']

	y_plt_data.plot().figure.savefig(save_path + 'yield_curve.png')
	
	# save stats
	stats = [ice_stat1, ice_stat2, ice_stat3, ice_stat4, ted_stat1, ted_stat2, ted_stat3,
	ls_stat1, ls_stat2, ls_stat3, fund_stat1, fund_stat2, ur_stat1, ur_stat2]

	lis = ["ice", "ted", "ls","fund", "ur"]
	times = (4, 3, 3, 2, 2)
	label = sum(([x]*y for x,y in zip(lis, times)),[])

	stat_df = pd.DataFrame({'label': label, 'stat': stats})
	stat_df.to_csv(save_path + "stat_df.txt", sep = "|", index = False)
