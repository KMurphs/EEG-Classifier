#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import os
from os import listdir
import numpy as np
import csv
import sys
from matplotlib import pyplot as plt
import pandas as pd
import pyedflib

from EEG_IIR_Filter_BPF import EEGFilter
from EEG_Feature_Extraction import getMMDFeature, geteSYSFeature



def Build_File_Pairs():
    PSGFiles = list()
    HYPFiles = list()
    #for item in listdir('..\\Data'):
    for item in listdir('Data'):
        if('.edf' in item):
            if('-Hypnogram' in item):
                HYPFiles.append(item)
            if('-PSG' in item):
                PSGFiles.append(item)	
			
	FilePairs = list()			
    for File in PSGFiles: 
        Temp = File[:6]
        for hypfile in HYPFiles:
            if(Temp in hypfile):
                FilePairs.append([File, hypfile])	
                break					
            
    return FilePairs


def Print_Counters(DictCounter):
    Total = 0
    for key in DictCounter.keys():
        Total = Total + DictCounter[key][0]
        print('Stage %s has %d Samples'%(key,DictCounter[key][0])) 
    print('File length is %d samples\n'%Total)
    
    Total = 0
    for key in DictCounter.keys():
        Total = Total + DictCounter[key][1]
        print('Stage %s has %d Epochs'%(key,DictCounter[key][1])) 
    print('File length is %d Epochs\n'%Total)




def Build_Dataset(PsgFile, HypFile, DictCounter):
    try:
        SampleFreq = 100
        EpochLengthSec = 10 
        N_EpochSubWindows = 10
        EpochLength = EpochLengthSec * SampleFreq
        
        #read edf files
#        f = pyedflib.EdfReader("../Data/" + PsgFile)
#        g = pyedflib.EdfReader("../Data/" + HypFile)
        f = pyedflib.EdfReader("Data/" + PsgFile)
        g = pyedflib.EdfReader("Data/" + HypFile)
        buf = f.readSignal(0)
        annotations = g.readAnnotations()
        annotation_length = len(annotations[1])
        f._close()
        del f
        g._close()
        del g 
        
        #combine sample and annotations
        i = 0
        j = 0
        dataset = list()
        for i in range(int(len(buf))):
            if(j+1 >= annotation_length):
                j = annotation_length - 1 - 1
            if(int(annotations[0][j+1]) == int((i/100))):
        	    j = j+1
            line = [buf[i],annotations[2][j]]
            i = i + 1		
            dataset.append(line)
        
        #extract whole set of epochs (1000 samples with the same class)
        Epochs = list()
        epoch = list()
        currentclass = dataset[0][1]
        for item in dataset:
            if (item[1] == currentclass):
                epoch.append(item)
                if(len(epoch) == EpochLength):
                    Epochs.append(epoch)
                    epoch = list()
            else:
                currentclass = item[1]
                epoch = list()
                
        print('There are %d Samples in file %s'%(len(dataset),PsgFile))
        print('There are %d Epochs in file %s'%(len(Epochs),PsgFile)) 
        print('Therefore, the number of samples kept is %d for file %s'%((len(Epochs) * EpochLength),PsgFile))           
          
        #filtering and feature extraction
        NewDataset = list()
        for epoch in Epochs:
            samples = list()
            for sample in epoch:
                samples.append(sample[0])
            Result = EEGFilter(samples, SampleFreq, Orders = [5,5,5,5,5])
            currentclass = sample[1]
            DictCounter = UpdateStageCounters(DictCounter, currentclass)
            DictCounter = UpdateSampleCounters(DictCounter, currentclass, len(samples))

            #extract features from each bands and bundle in epoch_feat
            epoch_feat = list()
            for key in Result.keys():
                BandData = Result[key][1]
                BandCenter = Result[key][0]
                MMDResult = getMMDFeature(BandData, SampleFreq, EpochLengthSec, N_EpochSubWindows)
                eSYSResult = geteSYSFeature(BandData, SampleFreq, EpochLengthSec, BandCenter)
                epoch_feat.append(MMDResult)
                epoch_feat.append(eSYSResult)       
            epoch_feat.append(currentclass)
            NewDataset.append(epoch_feat)
 
        #write new dataset in csv file               
        with open('data/EEGFeatureDataset.csv','ab') as CSVFile:
            writer = csv.writer(CSVFile)
            writer.writerows(NewDataset)           

        return DictCounter

    except:
        print('Error Occured while reading file %s'%PsgFile)
        with open('data/Errors.csv','ab') as CSVFile:
            CSVFile.write(PsgFile + "\n")
		


def ResetCounter(DictCounter):
    for key in DictCounter.keys():
        DictCounter[key] = [0,0]
    return DictCounter

def UpdateStageCounters(DictCounter, key):
    DictCounter[key][1] += 1
    return DictCounter

def UpdateSampleCounters(DictCounter, key, N):
    DictCounter[key][0] += N
    return DictCounter


    
def PrepareData(File):
    try:
        SampleFreq = 100
        EpochLengthSec = 10 
        N_EpochSubWindows = 10
        EpochLength = EpochLengthSec * SampleFreq
        
        #read csv file from internet and store on computer
        dataset = pd.read_csv(File, sep= ',', header= None)
        
        #extract whole set of epochs (1000 samples with the same class)
        Samples = dataset[0:EpochLength]
                        
        #filtering and feature extraction
        Result = EEGFilter(Samples, SampleFreq, Orders = [5,5,5,5,5])
          
        #plotting the filter result of a stage
        plotcounter = 711
        plt.subplot(plotcounter)
        plt.plot(range(len(Samples)), Samples, label = 'Original Data')
        plt.legend(loc = 'upper right', shadow = True)
        for key in Result.keys():
            plotcounter += 1
            plt.subplot(plotcounter)
            plt.plot(range(len(Samples)), Result.get(key)[1], label = key) 
            plt.legend(loc = 'upper right', shadow = True)
        plt.show()

        #extract features from each bands and bundle in epoch_feat
        epoch_feat = list()
        for key in Result.keys():
            BandData = Result[key][1]
            BandCenter = Result[key][0]
            MMDResult = getMMDFeature(BandData, SampleFreq, EpochLengthSec, N_EpochSubWindows)
            eSYSResult = geteSYSFeature(BandData, SampleFreq, EpochLengthSec, BandCenter)
            epoch_feat.append(MMDResult)
            epoch_feat.append(eSYSResult)                

        return epoch_feat

    except:
        print('Error Occured while reading file %s'%File)
        with open('data/Errors.csv','ab') as CSVFile:
            writer = csv.writer(CSVFile)
            writer.writerows([File,1]) 
            
            
            
            
def Process_EDF_Files():     
    print('\n\nProcessing EDF Files')
    
    file_pairs = Build_File_Pairs()  
    
    DictCounter = {'Sleep stage W':[0,0], 'Sleep stage 1':[0,0], 'Sleep stage 2':[0,0], 'Sleep stage 3':[0,0],'Sleep stage 4':[0,0], 'Sleep stage R':[0,0], 'Movement time':[0,0], 'Sleep stage ?':[0,0]}
    file_counter = 0
    for item in file_pairs:
        PSG = item[0]
        HYP = item[1]
        print('\n\n%d out of %d Appending:   PSG File: %s  and HYP File: %s'%(file_counter,len(file_pairs),PSG,HYP))
        Build_Dataset(PSG, HYP, DictCounter)
        file_counter += 1      
        
    Print_Counters(DictCounter)
        
        
        
        
        
if __name__ == '__main__':   
    DictCounter = {'Sleep stage W':[0,0], 'Sleep stage 1':[0,0], 'Sleep stage 2':[0,0], 'Sleep stage 3':[0,0],'Sleep stage 4':[0,0], 'Sleep stage R':[0,0], 'Movement time':[0,0], 'Sleep stage ?':[0,0]}
    DictCounter = ResetCounter(DictCounter)    
#w i sawake
#1,2,3,4 were combined into NREM1 NREM2 NREM3 (3 and 4 combined)
#R is REM
#Movement Time  is body movement usually after NREM 3 and before REM
    Process_EDF_Files    
