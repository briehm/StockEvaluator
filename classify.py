
import asset_time_series as at
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import argparse
from config import DATA_ROOT_DIR


import glob
import os

np.set_printoptions(threshold='nan')




year = 250
training_offset = 5
test_offest = 0


SVM = 0
RANDOM_FOREST = 1


#CLASSIFIER________________________


#RANDOM_TREE____________________________________

def train_random_forest(data):
    rdt = RandomForestClassifier(n_estimators=5, max_depth=2,min_samples_split=1, random_state=0)
    rdt.n_classes_ = 3
    y = []

    X = data[:,0:-1]
    z = data[:,-1]
    y = np.array(z)

    #print y
    #print "LABEL: " , len(y)
    rdt.fit(X, y)  
    return rdt


def predict_random_forest(rdt,data):    
    resut = rdt.predict(data)
   # print resut.shape
    return resut


#SVM_________________________________________
def train_SVM(data):
    clf = svm.SVC()
    X = data[:,0:-1]
    y = data[:,-1]
    clf.fit(X, y)  
    return clf


def predict_SVM(svm_,data):
    test = svm_.predict(data)
    print "SVM", test.shape
    return test
    #print "SVM SUP VEC" , svm_.support_vectors_.shape
    #return svm_.support_vectors_


def get_label(dates_):

    value = (dates_[0]-dates_[len(dates_)-1]) * 100.0/dates_[len(dates_)-1]
    #print value
    label = 0

    if value > 1.5:
        label = 1
    elif value < -1.0:
        label = -1

    return label    





def generate_trainings_data(dataframes,filenames):
    data = []
    for name in filenames:
        training_data = dataframes[name][test_offest:-1]
        for day in range(len((training_data)-training_offset)/6):
            if day>year:
                label = get_label(training_data[day-year:day-year+training_offset]["Close"])
               # print label
                from_ = training_offset+day-year
                until_ = day+training_offset+1
                features = at.get_performance_feature(training_data[from_:until_])
                #print features
                temp = np.append(features,label)
                data.append(temp) 


        
    print len(data)
    return np.array(data) 


def generate_test_data(dataframes,filenames):
    data = []
    for name in filenames:
        test_data = dataframes[name][0:test_offest]

        for day in range(len(test_data)):
            if day>=year:
                from_ = day-year
                until_ = day+1
                features = at.get_performance_feature(test_data[from_:until_])
                
                data.append(features) 

        
    print len(data)
    return np.array(data) 



def generate_test_features(dataframes,date,filenames):
    data = []

    for name in filenames:
       # print dataframes[name]
        if(date in dataframes[name].index):
            index = dataframes[name].index.get_loc(date)
       # test_data =np.where(dataframes[name].index==
            t_data = dataframes[name][index:len(dataframes[name])]
            features = at.get_performance_feature(t_data)
            
        else:
            features = np.zeros(4,)

        data.append(features) 

        
   # print data
    return np.array(data) 








def split_dataframes(dataframes,filenames):
    test_data = []
    training_data = []
    for name in filenames:
        print dataframes[name][0:2]
        test_data = np.append(test_data, dataframes[name][0:3])
        training_data = np.append(training_data,dataframes[name][3:-1])
    return test_data,training_data


def get_date_array(dataframes,filenames,s_date,t_frame):
    temp_name = ""
    #print dataframes["AES"].index
    for name in filenames:
        if(s_date in dataframes[name].index):
            temp_name = name
            
    if(temp_name != ""):
        index = dataframes[name].index.get_loc(s_date)
        if index-t_frame >=0:
            dates = dataframes[name].index[index-t_frame:index]
        else:
            print "Invalid date"
        #print "STOP", dates
        return dates
    else:
        print "Date not found"
        return 0

   





if __name__ == '__main__':
    #default_values
    time_frame = 30
    start_date = '20.08.2009'
    training_path = os.path.join(DATA_ROOT_DIR, 'Asset-Prices/')
    test_path = os.path.join(DATA_ROOT_DIR, 'Asset-Prices-test/')
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help='date for which you want to know if to buy, sell or hold')
    parser.add_argument("-f", help='time frame')
    parser.add_argument("-training", help='path to training data')
    parser.add_argument("-test", help='path to test data')
    args = parser.parse_args()
    if args.t:
        start_date = args.t
    if args.f:
        time_frame = int(args.f)
    if args.training:
        training_path = args.training
    if args.test:
        test_path = args.test


    files_training = at.get_all_filenames_from_path(training_path)

    files_test = at.get_all_filenames_from_path(test_path)
    

    
    names = {at.parse_code(fn) for fn in files_training}  
    dataframes_training = {at.parse_code(fn): at.load_timeseries_dataframe_from_file(fn) for fn in files_training}
    dataframes_test = {at.parse_code(fn): at.load_timeseries_dataframe_from_file(fn) for fn in files_test}

    results = np.zeros((len(names), time_frame ))

    date_array = get_date_array(dataframes_test,names,start_date,time_frame)


    data = generate_trainings_data(dataframes_training,names)
#
    

    if SVM:
        svm__ = train_SVM(data)

    if RANDOM_FOREST:
        rdf_ = train_random_forest(data)
        date_array = np.flipud(date_array)

    t = 0
    for date in date_array:
    
        
        print "Calculate for ", date
        #data_test = generate_test_data(all_dataframes,t,names)

        data_test = generate_test_features(dataframes_test,date,names)
        

        if SVM:
            result = predict_SVM(svm__,data_test)

        if RANDOM_FOREST:
            result = predict_random_forest(rdf_,data_test)
            #print result

        results[:,t]= result
        # for name in range(len(names)):
        #     if(t>0):
        #         if(result[name] == 1):
        #             if(results[name:t-1] ):

        #         elif(result[t] == -1):
        #             print "d"
        #         else:
        #             results[name][t-1] = result[t]

        t = t+1
    print results



