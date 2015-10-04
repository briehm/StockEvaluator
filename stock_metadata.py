# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os

from config import DATA_ROOT_DIR

class MetadataLoader(object):

    __metadata_cache = None
    __ticker_dict_cache = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MetadataLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def get_stock_metadata(self):
        if not self.__metadata_cache:
            self.create_metadata_cache()
        return self.__metadata_cache

    def create_metadata_cache(self):
        company_metadata_file = os.path.join(DATA_ROOT_DIR, 'Metadata/MetaData_SP500_edited.csv')
        self.__metadata_cache = pd.read_csv(company_metadata_file,
                                              sep=';',
                                              dtype={'id': np.int, 'Ticker': np.str,
                                                     'Company': np.str})
    def create_ticker_dict(self):
        metadata_df = self.get_stock_metadata()
        dic = dict(zip(metadata_df.id, metadata_df.Ticker))
        self.__ticker_dict_cache = dic

    def get_id_to_ticker_dict(self):
        if not self.__ticker_dict_cache:
            self.create_ticker_dict()
        return self.__ticker_dict_cache
