#!/usr/bin/python

import pip
from datetime import datetime
import os

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])       


# main definition
if __name__ == "__main__":
    
    # make directory
	save_path = os.getcwd() + "/data"
	log_path = os.getcwd() + "/log"
    
	if not os.path.isdir(save_path):
		os.mkdir(save_path)
        
	if not os.path.isdir(log_path):
		os.mkdir(log_path)

	packages = ['yfinance', 'pandas', 'requests', 're', 'numpy', 'matplotlib', 'PyMuPDF', 'notion', 'bs4', 'datetime', 'dateutil', 'fear_greed_index', 'cairosvg']

    # install packagke
	for p in packages:
		#print(p)
		import_or_install(p)
        
	today = datetime.today()
	today_str = str(today.strftime("%Y-%m-%d %H:%M:%S"))
	
	log_message1 = '1. setup'
	log_message2 = 'package install success.'
	log_message3 = '1. setup success'

	os.system( 'echo "==========================================" >> ' + log_path + '/economy_alert_log.txt' )
	os.system( 'echo "' + today_str + ' logging." >> ' + log_path + '/economy_alert_log.txt' )
	os.system( 'echo "' + log_message1 + '" >> ' + log_path + '/economy_alert_log.txt' )
	os.system( 'echo "' + log_message2 + '" >> ' + log_path + '/economy_alert_log.txt' )
	os.system( 'echo "' + log_message3 + '" >> ' + log_path + '/economy_alert_log.txt' )
