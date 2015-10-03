

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from wordcloud import WordCloud


import glob
import os

#asset_ts_folder = '/home/till/devel/python/hz15_tsdata/Asset-Prices/'
#asset_ts_folder = '/Users/Seb/Stockdata/Asset-Prices/'
asset_ts_folder =  '/Users/benedikt/Documents/Coding/StockEvaluator/Asset-Prices/'

#generate features
def get_interday_performance(stock_hist):

    interday_open = stock_hist["Open"].values[0]
    interday_close = stock_hist["Close"].values[0]
    perc = 100.0/interday_open * (interday_close-interday_open)
    return perc


def get_week_performance(stock_close):

    latest_value = stock_close.values[0]
    if(len(stock_close)>=5):
        week_ago = stock_close.values[5]
        perc_1 = 100.0/week_ago * (latest_value-week_ago)
    elif
        prec_1 = 0
    return perc_1


def get_month_performance(stock_close):
    latest_value = stock_close.values[0]
    if(len(stock_close)>=25):
        month_ago = stock_close.values[25]
        perc_2 = 100.0/month_ago * (latest_value-month_ago)
    elif
        perc_2 = 0
    return perc_2

def get_year_performance(stock_close):
    latest_value = lc.values[0]
    if(len(stock_close)>=250):
        year_ago = stock_close.values[250]
        perc_3 = 100.0/year_ago * (latest_value-year_ago)
    elif
        perc_3 = 0
    return perc_3


def get_performance_feature(stock_history):
    close = stock_history[["Close"]]
    features = []
    features = np.append(features, get_interday_performance(stock_history))
    features = np.append(features, get_week_performance(close))
    features = np.append(features, get_month_performance(close))
    features = np.append(features, get_year_performance(close))
              
    return features
#END generate features


#Plot Graphs
def draw_plot(stock_history,name):
    #print stock_history[[0]]
    plotHandle = plt.plot(pd.to_datetime(stock_history.index,dayfirst=True),stock_history[["Close"]])
    red_patch = mpatches.Patch(color='blue', label=name)
    plt.legend(handles=[red_patch])
    plt.xlabel('Years', fontsize=18)
    plt.ylabel('Value', fontsize=16)
    plotHandle.annotate('M&A event', xy=(10, 10), xytext=(10, 20),
            arrowprops=dict(facecolor='red', shrink=0.05))
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
    plt.subfigure().imshow(wordcloud).axis("off").show()

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
