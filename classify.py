

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm

import glob
import os



#generate features
def svm_():
    X = [[0, 0], [1, 1]]
    y = [-1,0, 1]
    clf = svm.SVC()
    clf.fit(X, y)  
    clf.predict([[2., 2.]])
    print clf.support_vectors_



if __name__ == '__main__':
    svm_()
