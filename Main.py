# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 12:03:47 2017

@author: kibs
"""
import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

filepath = os.path.dirname(os.path.realpath(__file__))
if filepath not in sys.path:
    sys.path.insert(0,filepath)

dependencies = os.path.join(filepath,"Dependencies")
if dependencies not in sys.path:
    sys.path.insert(0,dependencies)



from FileHandler import Download_EDF_Files
from Process_EDF_Files import Process_EDF_Files
from Process_Columns import *
from Report import ReportResult

from pandas.plotting import scatter_matrix
import seaborn as sns
import matplotlib as plt


#importing all the required ML packages
from sklearn.linear_model import LogisticRegression #logistic regression
from sklearn import svm #support vector Machine
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.neighbors import KNeighborsClassifier #KNN
from sklearn.naive_bayes import GaussianNB #Naive bayes
from sklearn.tree import DecisionTreeClassifier #Decision Tree
from sklearn.model_selection import train_test_split #training and testing data split
from sklearn import metrics #accuracy measure
from sklearn.metrics import confusion_matrix #for confusion matrix


from sklearn.model_selection import KFold #for K-fold cross validation
from sklearn.model_selection import cross_val_score #score evaluation
from sklearn.model_selection import cross_val_predict #prediction

from sklearn.model_selection import GridSearchCV

from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier




EEGFiles_url = 'https://physionet.org/physiobank/database/sleep-edfx/'
columns_name = ['Delta_MMD','Delta_eSYS','Theta_MMD','Theta_eSYS','Alpha_MMD','Alpha_eSYS','Beta_MMD','Beta_eSYS','Gamma_MMD','Gamma_eSYS', 'target']
download_file = False

if __name__ == '__main__':
    
    if(download_file):
        Download_EDF_Files(EEGFiles_url)
        Process_EDF_Files()
        data = pd.read_csv('Data\EEGFeatureDataset.csv', delimiter = ',', names = columns_name) 
        for col in columns_name:
            if col == 'target':
                data = Process_Targets(data, col)
            else:
                data[col] = Standardize_Col(data, col)  
        data.to_csv('Data\EEGDataset_Standardized.csv')
    
    
    data = pd.read_csv('Data\EEGDataset_Standardized.csv', delimiter = ',') 
   
    print('Learning Data...')
    X = data.values[:,0:10]
    Y = data['Sleep stage W']
    X_train,X_test,Y_train,Y_test = train_test_split(X, Y, test_size = 0.3, stratify = Y)
    
    models = {'Random Forest': RandomForestClassifier(n_estimators=100),
              'Logistic Regression': LogisticRegression(), #poor Results: 59% accuracy
              'K - Nearest Neighbours': KNeighborsClassifier(),
              'Gradient Boosting': GradientBoostingClassifier(n_estimators=100),
              'Naive Bayes Classifier': GaussianNB(),
            }
    
    for model in models:
        models[model].fit(X_train,Y_train)
        prediction7 = models[model].predict(X_test)
        print('\nThe accuracy of the %s is %.2f%%'%(model, metrics.accuracy_score(prediction7,Y_test)*100))
        ReportResult(list(Y_test), list(prediction7))