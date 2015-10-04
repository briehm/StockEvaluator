
import asset_time_series as at
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

import glob
import os

time_frame = 30
start_time = 1
end_time = start_time + time_frame



year = 250
training_offset = 10
test_offest = 0


SVM = 0
RANDOM_FOREST = 1


#CLASSIFIER________________________


#RANDOM_TREE____________________________________

def train_random_forest(data):
    rdt = RandomForestClassifier(n_estimators=5, max_depth=2,min_samples_split=1, random_state=0)
    rdt.n_classes_ = 3
    y = []
    print data.shape
    X = data[:,0:-1]
    z = data[:,-1]
    y = np.array(z)

    #print y
    #print "LABEL: " , len(y)
    rdt.fit(X, y)  
    return rdt


def predict_random_forest(rdt,data):    
    resut = rdt.predict(data)
    print resut.shape
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
    print "SVM SHAOE", test.shape
    return test
    #print "SVM SUP VEC" , svm_.support_vectors_.shape
    #return svm_.support_vectors_


def get_label(dates_):

    value = (dates_[0]-dates_[len(dates_)-1]) * 100.0/dates_[len(dates_)-1]
    label = 0

    if value > 1:
        label = 1
    elif value < -1:
        label = -1

    return label    





def generate_trainings_data(dataframes,filenames):
    data = []
    for name in filenames:
        training_data = dataframes[name][test_offest:-1]
        print training_data
        for day in range(len((training_data)-training_offset)/6):
            if day>year:
                label = get_label(training_data[day-year:day-year+training_offset]["Close"])
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
        test_data = dataframes[name].index
        break
        for day in range(len(test_data)):
            if day>=year:
                from_ = day-year
                until_ = day+1
                features = at.get_performance_feature(test_data[from_:until_])
                
                data.append(features) 

        
    print len(data)
    return np.array(data) 








def split_dataframes(dataframes,filenames):
    test_data = []
    training_data = []
    for name in filenames:
        print dataframes[name][0:2]
        test_data = np.append(test_data, dataframes[name][0:3])
        training_data = np.append(training_data,dataframes[name][3:-1])
    return test_data,training_data




if __name__ == '__main__':
    files = at.get_all_filenames_old()
    results = np.zeros((len(files), 30))

    
    names = {at.parse_code(fn) for fn in files}  
    all_dataframes = {at.parse_code(fn): at.load_data_frame_from_file(fn) for fn in files}

    data = generate_trainings_data(all_dataframes,names)

    if SVM:
        svm__ = train_SVM(data)

    if RANDOM_FOREST:
        rdf_ = train_random_forest(data)

    

    for t in range(time_frame):

        print result.shape
        print result     

        #data_test = generate_test_data(all_dataframes,t,names)

        data_test = generate_test_features(all_dataframes,t,names)
        

        if SVM:
            result = predict_SVM(svm__,data_test)

        if RANDOM_FOREST:
            result = predict_random_forest(rdf_,data_test)

        results[:,t]= result


