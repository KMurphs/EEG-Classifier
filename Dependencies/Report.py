# -*- coding: utf-8 -*-
"""
Created on Thu Jan 04 08:15:09 2018

@author: kibs
"""

import datetime
import time
from sklearn.metrics import accuracy_score

def ReportResult(Target, Prediction):
    ReportFile = open('Data\Report.txt','a')
    strTemp = datetime.datetime.now() 
    strTemp = '\n\n--------------%s\n'%strTemp
    ReportFile.write(strTemp)
    
    Accuracy = accuracy_score(Target,Prediction)*100
    strAccuracy = "Overall Accuracy is {:.2f}%%".format(Accuracy)
    print(strAccuracy)    
    ReportFile.write(strAccuracy + '\n')

    stage = 'Sleep stage W'

    W = [0,0,0,0,len(Target)]
    for counter in range(len(Target)):
        if((Target[counter] == 1) and (Prediction[counter] == 1)):
            W[0] += 1 #true pos
        elif((Target[counter] != 1) and (Prediction[counter] != 1)):
            W[1] += 1 #true neg
        elif ((Target[counter] == 1) and (Prediction[counter] != 1)):
            W[2] += 1 #false neg
        elif ((Target[counter] != 1) and (Prediction[counter] == 1)):
            W[3] += 1 #false pos     
        
    # these formulas can be found @ https://en.wikipedia.org/wiki/Sensitivity_and_specificity
    strTemp = 'Stage: {}'.format(stage)
    print(strTemp)
    ReportFile.write(strTemp + '\n')    

    strTemp = '   Accuracy: %.2f%%'%((W[0]+W[1])*100/float(W[4]))
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    strTemp = '   Sensitivity: %.2f%%'%(W[0]*100/float(W[0]+W[2]))
    print(strTemp)
    ReportFile.write(strTemp + '\n')
    
    strTemp = '   Specificity: %.2f%%'%(W[1]*100/float(W[1]+W[3]))
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    strTemp = '   Precision: %.2f%%'%(W[0]*100/float(W[0]+W[3]))
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    for counter in range(len(W)):
        W[counter] = W[counter]*100/float(W[4])
        
    strTemp = '   True Positive: %.2f%%'%W[0]
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    strTemp = '   True Negative: %.2f%%'%W[1]
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    strTemp = '   False Negative: %.2f%%'%W[2]
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    strTemp = '   False Positive: %.2f%%'%W[3]
    print(strTemp)
    ReportFile.write(strTemp + '\n') 
    
    ReportFile.close()