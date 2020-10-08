# load data
import os
import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def economy_line_plot(data, month, standard, title, xlab, ylab, save_path, save_name):
    fig = plt.figure()
    plt.suptitle('ggplot style')
    
    newest_date =  data.date.tail(n=1).values[0]
    newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()
    
    three_month = newest_datetime - relativedelta(months = month)
    three_month_f = three_month.strftime("%Y-%m-%d")

    try:
        three_month_data = data.loc[np.where(data.date == three_month_f)[0][0]:,:]
    except:
        three_month_data = data.tail(n = month*30)

    three_month_data.date =  pd.to_datetime(three_month_data.date, format='%Y-%m-%d')

    plt.plot(three_month_data.date, three_month_data.value)
    plt.axhline(y = standard, color = 'r')

    fig.suptitle(title, fontsize = 20)
    plt.xlabel(xlab, fontsize = 16)
    plt.ylabel(ylab, fontsize = 16)
    fig.savefig(save_path + save_name)
    
def get_newest_stat(data):
    newest_value = data.value.tail(n=1).values[0]
    
    return newest_value

def last_value_stat(data, month):
    newest_date =  data.date.tail(n=1).values[0]
    newest_datetime = datetime.strptime(newest_date, "%Y-%m-%d").date()
    newest_value = data.value.tail(n=1).values[0]

    # last month
    last_month = newest_datetime - relativedelta(months = month)
    last_month_f = last_month.strftime("%Y-%m-%d")

    try: 
        last_month_value = data.loc[data.date == last_month_f,:].value.values[0]
    except:
        last_month_value = data.tail(n = month*30).value.values[0]

    stat1 = (newest_value - last_month_value) / last_month_value
    
    return round(stat1,2)


# main definition
if __name__ == "__main__":
    data_dir = "/Users/jongwon/python/economy/macro_economy/data/"
    files = os.listdir(data_dir)

    txt_regex = re.compile('.txt$')
    png_regex = re.compile('.png$')

    txt_file = list(filter(txt_regex.search, files))
    png_file = list(filter(png_regex.search, files))

    # text file
    for txt in txt_file:
        file = data_dir + txt
        data = pd.read_csv(file, sep = "|")

        # data type change
        data.value = data.value.replace(".", None)
        data = data.loc[data.value != ".",:]
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
                             save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                             save_name = "ICE")
        elif txt == "TEDRATE.txt":
            ted_stat1 = get_newest_stat(data)
            ted_stat2 = last_value_stat(data, month = 1)
            ted_stat3 = last_value_stat(data, month = 3)
            
            economy_line_plot(data, month = 6, standard = 1,
                     title = "TED-6month", xlab = "date", ylab = "value",
                     save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                     save_name = "TED")
            
        elif txt == "T10Y2Y.txt":
            ls_stat1 = get_newest_stat(data)
            ls_stat2 = last_value_stat(data, month = 1)
            ls_stat3 = last_value_stat(data, month = 3)
            
            economy_line_plot(data, month = 6, standard = 0,
                     title = "LS-6month", xlab = "date", ylab = "value",
                     save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                     save_name = "LS")
        elif txt == "FEDFUNDS.txt":
            fund_stat1 = get_newest_stat(data)
            fund_stat2 = last_value_stat(data, month = 1)
            
            economy_line_plot(data, month = 12, standard = 0,
                     title = "funds-1year", xlab = "date", ylab = "value",
                     save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                     save_name = "funds_rate")
        elif txt == "UNRATE.txt":
            ur_stat1 = get_newest_stat(data)
            ur_stat2 = last_value_stat(data, month = 2)
            
            economy_line_plot(data, month = 6, standard = 0,
                     title = "unrate-6month", xlab = "date", ylab = "value",
                     save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                     save_name = "unrate")
        else:
            economy_line_plot(data, month = 1, standard = 2,
                     title = "price-1month", xlab = "date", ylab = "value",
                     save_path = "/Users/jongwon/python/economy/macro_economy/plot/",
                     save_name = "price")

    # save stats
    stats = [ice_stat1, ice_stat2, ice_stat3, ice_stat4, ted_stat1, ted_stat2, ted_stat3,
    ls_stat1, ls_stat2, ls_stat3, fund_stat1, fund_stat2, ur_stat1, ur_stat2]

    lis = ["ice", "ted", "ls","fund", "ur"]
    times = (4, 3, 3, 2, 2)
    label = sum(([x]*y for x,y in zip(lis, times)),[])

    stat_df = pd.DataFrame({'label': label, 'stat': stats})
    stat_df.to_csv("/Users/jongwon/python/economy/macro_economy/plot/stat_df.txt", sep = "|", index = False)