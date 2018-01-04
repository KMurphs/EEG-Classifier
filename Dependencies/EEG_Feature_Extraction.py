# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 19:46:12 2017

@author: Lab1
"""

import math
import numpy as np
from matplotlib import pyplot as plt

def getMMDFeature(x, SampleFreq = 100, EpochLengthSec = 10, N_EpochSubWindows = 10):
    minValue = float('Inf')
    maxValue = float('-Inf')
    minIndex = -1
    maxIndex = -1
    Index = 0
    
    SubWindowLength = EpochLengthSec * SampleFreq / N_EpochSubWindows
    
    
    NextSliceStart = 0
    xSlices = list()
    
    for Slice in range(len(x)/SubWindowLength):
        NextSliceStop = NextSliceStart + SubWindowLength - 1
        if(NextSliceStop > len(x)):
            NextSliceStop = len(x)
        xSlices.append(x[NextSliceStart : NextSliceStop])
        NextSliceStart = NextSliceStart + SubWindowLength
        
    if((len(x) - 1) > NextSliceStart):
        xSlices.append(x[NextSliceStart : len(x)])
    
    MMDs = list()
    for Slice in xSlices:
        for value in Slice:
            if (minValue > value):
                minValue = value
                minIndex = Index       
            if (maxValue < value):
                maxValue = value
                maxIndex = Index       
            Index += 1   
        deltaValue = (maxValue - minValue)**2
        deltaIndex = (maxIndex - minIndex)**2
        MMDs.append((deltaValue + deltaIndex)**0.5)
    
    MMDFeature = 0
    for MMD in MMDs:
        MMDFeature = MMDFeature + MMD
       
    Result = [MMDFeature, len(xSlices)]
    return MMDFeature
       
def geteSYSFeature(x, SampleFreq = 100, EpochLengthSec = 10, MidBandFreq = 5):
    Temp = 0
    for value in x:
        Temp = Temp + (value**2)
        
    N = SampleFreq * EpochLengthSec
    wavelength = 100
    if(N >= 10000):
        wavelength = 10 ** ((math.log(N,10)) - 1)
        
    eSYSFeature = Temp * MidBandFreq * wavelength
    
    return eSYSFeature


if __name__ == '__main__':
    t = np.linspace(0, 10, 1001)
    x = np.sin(2 * np.pi * t)
    
    print(getMMDFeature(x,100,10,10))
    print(geteSYSFeature(x,100,10,10))
    
    plt.plot(t,x, label = 'Data')