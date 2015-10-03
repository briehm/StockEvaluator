

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


import glob
import os

#asset_ts_folder = '/home/till/devel/python/hz15_tsdata/Asset-Prices/'
asset_ts_folder = '/Users/Seb/Stockdata/Asset-Prices/'

#generate features
def get_week_performance(stock_close):

    latest_value = stock_close.values[0]
    week_ago = stock_close.values[6]
    perc_1 = 100.0/week_ago * (latest_value-week_ago)
    return perc_1


def get_month_performance(stock_close):
    latest_value = stock_close.values[0]
    month_ago = stock_close.values[25]
    perc_2 = 100.0/month_ago * (latest_value-month_ago)
    return perc_2

def get_year_performance(stock_close):
    latest_value = stock_close.values[0]
    year_ago = stock_close.values[250]
    perc_3 = 100.0/year_ago * (latest_value-year_ago)
    return perc_3


def get_performance_feature(stock_history):
    close = stock_history[["Close"]]
    features = []
    features = np.append(features, get_week_performance(close))
    features = np.append(features, get_month_performance(close))
    features = np.append(features, get_year_performance(close))
              
    return features
#END generate features


#Plot Graphs
def draw_plot(stock_history,name):
    #print stock_history[[0]]
    plt.plot(pd.to_datetime(stock_history.index,dayfirst=True),stock_history[["Close"]])
    red_patch = mpatches.Patch(color='blue', label=name)
    plt.legend(handles=[red_patch])
    plt.xlabel('Years', fontsize=18)
    plt.ylabel('Value', fontsize=16)
    return plt

#End Plot Graphs



def load_data_frame_from_file(filename):
    return pd.read_csv(filename, infer_datetime_format=True, index_col=0)

def load_stock_history(id, ticker_symbol):
    name = os.path.join(asset_ts_folder, str(id)+"_"+ticker_symbol+'.csv')
    return load_data_frame_from_file(name)

def get_all_filenames():
    return glob.glob(os.path.join(asset_ts_folder, '*.csv'))

def parse_code(filename):
    basename = os.path.basename(filename)
    return basename.split('.')[0].split('_')[1]

def get_asset_price_feature_vector(asset, time):
    pass

if __name__ == '__main__':
    files = get_all_filenames()
    # all_dataframes = {parse_code(fn): load_data_frame_from_file(fn) for fn in files}
    history = load_stock_history(9, "AES")
    print history
    feature = get_performance_feature(history)
    print feature
    pl = draw_plot(history,"AES")
    pl.show()
