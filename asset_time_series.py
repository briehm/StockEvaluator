

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
#from wordcloud import WordCloud
import argparse

from stock_metadata import MetadataLoader

from config import DATA_ROOT_DIR

import glob
import os

asset_ts_folder = os.path.join(DATA_ROOT_DIR, 'Asset-Prices/')

#generate features
def get_interday_performance(stock_hist):
    perc = 0
    if(len(stock_hist)>=0):
        interday_open = stock_hist["Open"].values[0]
        interday_close = stock_hist["Close"].values[0]
        perc = 100.0/interday_open * (interday_close-interday_open)

    return perc


def get_week_performance(stock_close):

    perc_1 = 0
    if(len(stock_close)>5):
        latest_value = stock_close.values[0]   
        week_ago = stock_close.values[5]
        perc_1 = 100.0/week_ago * (latest_value-week_ago)

    return perc_1


def get_month_performance(stock_close):

    perc_2 = 0
    if(len(stock_close)>25):
        latest_value = stock_close.values[0]
        month_ago = stock_close.values[25]
        perc_2 = 100.0/month_ago * (latest_value-month_ago)

    return perc_2

def get_year_performance(stock_close):
    perc_3 = 0
    if(len(stock_close)>250):
        latest_value = stock_close.values[0]
        year_ago = stock_close.values[250]
        perc_3 = 100.0/year_ago * (latest_value-year_ago)
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
    plotHandle = plt.plot(pd.to_datetime(stock_history.index,dayfirst=True), stock_history[["Close"]])
    red_patch = mpatches.Patch(color='blue', label=name)
    plt.legend(handles=[red_patch])
    plt.xlabel('Years', fontsize=18)
    plt.ylabel('Value', fontsize=16)
    plt.title(name)
    #plotHandle.annotate('M&A event', xy=(10, 10), xytext=(10, 20), arrowprops=dict(facecolor='red', shrink=0.05))
    #for week in stock_history.index, STEPS
    #    if abs( get_week_performance(stock_history[week]) ) > 5 %
    #        get doc from company in t=week
    #        -> generate wordcloud at position x=week

    #wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
    #plt.subfigure().imshow(wordcloud).axis("off").show()

    return plt

#End Plot Graphs



def load_timeseries_dataframe_from_file(filename):
    return pd.read_csv(filename, infer_datetime_format=True, index_col=0)

# def load_stock_history(id, ticker_symbol):
#     name = os.path.join(asset_ts_folder, str(id)+"_"+ticker_symbol+'.csv')
#     return load_data_frame_from_file(name)

def load_stock_history(ticker_symbol):
    id_ = ''
    for filename in get_all_filenames():
        if ticker_symbol in filename:
            id_ = filename.split('_')[0]
            print id_
            break
    if id_:
        name = os.path.join(asset_ts_folder, "{}_{}.csv".format(id_, ticker_symbol))
        return load_timeseries_dataframe_from_file(name)
    else:
        return None


def load_stock_history_from_id(stock_id):
    stock_ticker_dict = MetadataLoader().get_id_to_ticker_dict()
    try:
        ticker_symbol = stock_ticker_dict[stock_id]
    except KeyError as ke:
        print "Invalid Stock ID {}".format(stock_id)
        return None

    ts_filename = os.path.join(asset_ts_folder, "{}_{}.csv".format(stock_id, ticker_symbol))
    return load_timeseries_dataframe_from_file(ts_filename)

def get_all_filenames():
    full_names = glob.glob(os.path.join(asset_ts_folder, '*.csv'))
    return [os.path.basename(name) for name in full_names]

def get_all_full_filenames():
    return glob.glob(os.path.join(asset_ts_folder, '*.csv'))

def get_all_filenames_from_path(path_):
    return glob.glob(os.path.join(path_, '*.csv'))

def parse_code(filename):
    basename = os.path.basename(filename)
    return basename.split('.')[0].split('_')[1]

def get_asset_price_feature_vector(asset, time):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help='The Ticker Symbol of the Stock to display, e.g. GOOGL')
    args = parser.parse_args()
    if args.s:
        history = load_stock_history(args.s)

        # all_dataframes = {parse_code(fn): load_data_frame_from_file(fn) for fn in files}
        # history = load_stock_history(9, "AES")
        if history is not None:
            feature = get_performance_feature(history)
            pl = draw_plot(history, args.s)
            pl.show()
        else:
            print "Please provide a valid ticker code"
    else:
        print 'Please provide a Stock Ticker Code with -s'