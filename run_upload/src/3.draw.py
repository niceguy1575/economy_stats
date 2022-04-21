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
import chart_studio
import chart_studio.plotly as py

from plotly.offline import plot
from plotly import graph_objects as go
from plotly import express as px

def draw_plotly_line(data):
	fig = px.line(data, x = 'date', y ='value')
	return fig

# main definition
if __name__ == "__main__":
	
	save_path = "/home/ec2-user/economyAlert/data"
	log_path = "/home/ec2-user/economyAlert/log"
	today = datetime.today()
	today_str = str(today.strftime("%Y-%m-%d"))
	
	data_dir = save_path + "/"
	files = os.listdir(data_dir)

	txt_regex = re.compile('fred')

	txt_file = list(filter(txt_regex.search, files))
	
	chartstudio_api_id = ''
	chartstudio_api_key = ''
	
	log_message1 = '3. draw'
	os.system( 'echo "' + log_message1 + '" >> ' + log_path + '/economy_alert_log.txt' )
	# text file
	for txt in txt_file:

		log_message2 = '3-1. ' + txt
		os.system( 'echo "' + log_message2 + '" >> ' + log_path + '/economy_alert_log.txt' )

		file = data_dir + txt
		data = pd.read_csv(file, sep = "|")

		# data type change
		data.value = data.value.replace(".", None)
		data = data.loc[data.value != ".",:].copy()
		data.value = data.value.astype(float)

		# draw plot
		chart = draw_plotly_line(data)

		# upload to char studio
		chart_layer = txt
		chart_studio.tools.set_credentials_file(username = chartstudio_api_id, api_key = chartstudio_api_key)

		# 62, 65, 67, 69
		chart = py.plot(chart, filename = chart_layer, auto_open = False, fileopt = 'overwrite', sharing = 'public')
	
	log_message3 = '3. draw success'
	os.system( 'echo "' + log_message3 + '" >> ' + log_path + '/economy_alert_log.txt' )