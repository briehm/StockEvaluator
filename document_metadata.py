
import pandas as pd
import numpy as np
import os
from collections import Counter

document_metadata_path = '/home/till/devel/python/hz15_tsdata/Metadata/MetaData_documents_2004_2010.csv'

def get_all_metadata():
    big_df = pd.read_csv(document_metadata_path,
                         sep=';',
                         dtype={'id': np.int, 'FileID': np.int,
                                'filename': np.str, 'relativeFilepath': np.str,
                                'source': np.str, 'Weblink': np.str,
                                'NewsDate': np.str, 'CompanyName': np.str,
                                'CompanyTicker': np.str, 'Label': np.str},
                         infer_datetime_format=True)

    big_df.NewsDate = pd.to_datetime(big_df.NewsDate, infer_datetime_format=True)
    return big_df


def get_docs_by_source(source_):
    big_df = get_all_metadata()
    return big_df[(big_df.source == source_)]

if __name__ == '__main__':
    big_df = get_all_metadata()
    ct = Counter(big_df.Label)


