# -*- coding: utf-8 -*-
__author__ = 'till'


from asset_time_series import load_stock_history_from_id, get_interday_performance
from config import DATA_ROOT_DIR
from document_metadata import get_all_metadata
from itertools import izip
import os
import json

def get_stock_value_at_time(time, stock_id):
    stock_hist = load_stock_history_from_id(stock_id)
    try:
        idx = stock_hist.index.get_loc(time)
    except KeyError as ke:
        return None
    return stock_hist.ix[idx]

def estimate_performance(day_info):
    return 100.0/day_info.Open * (day_info.Close-day_info.Open)


matches_file = os.path.join(DATA_ROOT_DIR, 'matches.json')
matches = json.load(open(matches_file))
doc_metadata = get_all_metadata()

dates = [d.split('/') for d in doc_metadata.Weblink]
file_dates = dict(izip(list(doc_metadata.id), dates))

for (comp_id, doc_id) in matches[500:520]:
    print (comp_id, doc_id)
    print file_dates[doc_id]

# WORK IN PROGRESS.
# THE MISSING DATE LABELS FOR THE BLOOMBERG DATASET ARE A P.I.T.A.

