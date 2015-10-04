# -*- coding: utf-8 -*-
__author__ = 'till'


import pandas as pd
import numpy as np

import json
import os
import document_metadata

from collections import Counter
from itertools import izip

from config import DATA_ROOT_DIR
from businessweek_parser import parse_businessweek_file, tokenize_article, clean_company_name, parse_businessweek_url

from stock_metadata import MetadataLoader
NUM_TEXTFILES = 150000

if __name__ == "__main__":

    # 0.Step : get names of companies:

    company_df = MetadataLoader().get_stock_metadata()

    company_names = [clean_company_name(c) for c in company_df.Company]
    company_id_dict = dict(zip(company_names, company_df.id))
    company_name_set = set(company_names)

    # 1. step : count words and trigrams in the data set

    doc_data = document_metadata.get_docs_by_source('Bloomberg')

    uni_counter = Counter()
    bi_counter = Counter()

    matches = []

    for filename, doc_id in zip(doc_data.relativeFilepath, doc_data.FileID)[0:NUM_TEXTFILES]:
        filename = filename.replace('\\', '/')
        filename = os.path.join(DATA_ROOT_DIR, filename[1:])
        headline, text = parse_businessweek_file(filename)
        text = headline + "\n" + text

        found_companys = [cn for cn in company_names if cn in text]

        if any(found_companys):
            unigrams, bigrams = tokenize_article(text)

            uni_counter.update(unigrams)
            bi_counter.update(bigrams)

            for match in found_companys:
                matches.append((company_id_dict[match], doc_id))
                print "Found Match: {} appears in document {}.".format(match, doc_id)

    unigram_file = os.path.join(DATA_ROOT_DIR, 'unigrams.json')
    bigram_file = os.path.join(DATA_ROOT_DIR, 'bigrams.json')
    matches_file = os.path.join(DATA_ROOT_DIR, 'matches.json')

    with open(unigram_file, 'w') as fp:
        json.dump(dict(uni_counter), fp)

    with open(bigram_file, 'w') as fp:
        json.dump(dict(bi_counter), fp)

    with open(matches_file, 'w') as fp:
        json.dump(matches, fp)