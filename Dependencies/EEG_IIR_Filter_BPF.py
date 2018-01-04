# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 11:15:27 2017

@author: Lab1
"""

from scipy import signal
import numpy as np
from matplotlib import pyplot as plt


def IIRFilter(Xin, Wcl, Wch, Wsample = 100, Order = 5):
#    Wp = [0.270,0.333] #cutoff freq, normalized freq (nyquist freq =smaple feq /2 = 1)
#    Ws = [0.230,0.373] #stop freq, normalized freq (nyquist freq =smaple feq /2 = 1)
    Freq_nyq = Wsample / 2.0
    Wp = [Wcl/float(Freq_nyq),Wch/float(Freq_nyq)]    
    b, a = signal.butter(Order, [Wp[0],Wp[1]], 'bandpass', analog=False)

    Yout = signal.filtfilt(b,a, Xin)
    
    Result = list()
    Result.append((Wcl + Wch)/ 2.0)
    Result.append(Yout)

    return Result


def EEGFilter(x,SampleFreq,Orders):
    y1 = IIRFilter(x,1,4,SampleFreq,Orders[0])
    y2 = IIRFilter(x,4,8,SampleFreq,Orders[0])
    y3 = IIRFilter(x,8,13,SampleFreq,Orders[0])
    y4 = IIRFilter(x,13,22,SampleFreq,Orders[0])
    y5 = IIRFilter(x,30,45,SampleFreq,Orders[0])
    
    Result = {'Delta':y1,'Theta':y2,'Alpha':y3,'Beta':y4,'Gamma':y5}
    return Result

if __name__=='__main__':
    t = np.linspace(0, 1.0, 101)
    xlow = np.sin(2 * np.pi * 5 * t)
    xhigh = np.sin(2 * np.pi * 250 * t)
    x = xlow + xhigh
    
    Result = {'Delta':1,'Theta':1,'Alpha':1,'Beta':1,'Gamma':1}
    string = ''
    for key in Result.keys():
        string = string + str(key) + ',' + str(key) + ','
    print(string)