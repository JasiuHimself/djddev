#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import numpy as np
from scipy.signal import butter, lfilter
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation

import math


def column(matrix, i):
    return [row[i] for row in matrix]

def norm(vector1, vector2, vector3, cutDC = False, N = 500):
    norm = []
    for i in range(len(vector1)):
         norm.append(math.sqrt(pow(vector1[i],2)+pow(vector2[i],2)+pow(vector3[i],2)))
    return norm

def normWithoutDC(norm, N):
    normWithoutDC = []
    for n in range(0, len(norm)):
        for l in range(0,N):
            sumator = norm[n-l]
        normWithoutDC.append(norm[n]-((1.0/N)*sumator))
    return normWithoutDC

#aka srednia arytmetyczna
def signalEnergy(signal,N):
    sumator = 0
    for n in range(0,N):
        print sumator
        sumator += signal[n]
    return (1.0/N)*sumator

def signalVariance(signal,N):
    sumator = 0
    meanValue = signalEnergy(signal,N) #signal mean value
    for n in range(0, N):
        sumator += pow((signal[n] - meanValue),2)
    return (1.0/N)*sumator


def okienko(signal,windowWidth, overlappingPercent =0):
    overlapping = (int)(overlappingPercent/100.0*windowWidth)
    print overlapping
    windowBegining=0;
    plt.show()
    while (windowBegining<=len(signal)):
        plt.plot(signal[windowBegining:windowBegining+windowWidth],"r-")
        windowBegining = windowBegining + windowWidth - overlapping



# chce 2.5 sekundy f=200 wiec biere n=500
# wielkość okna analizy
N = 500
# Filter requirements.
order = 10  # rzad order
fs = 199      # sample rate, Hz
cutoff = 15 # desired cutoff frequency of the filter, Hz
# Get the filter coefficients so we can check its frequency response.




# dataFile = open('data/accelerometerWalkOnly.csv', 'r')
dataFile = open('test.csv', 'r')
vector = []
while True:
    line = dataFile.readline();
    if not line: break
    line = line.rstrip()
    vector.append([float(x) for x in line.split(';')])

dataFile.close



time = column(vector,0)
accX = column(vector,1)
accY = column(vector,2)
accZ = column(vector,3)


# 200 hz
def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

b, a = butter_lowpass(cutoff, fs, order)

accXFiltered = butter_lowpass_filter(accX,cutoff,fs,order)
accYFiltered = butter_lowpass_filter(accY,cutoff,fs,order)
accZFiltered = butter_lowpass_filter(accZ,cutoff,fs,order)
accNorm = norm(accXFiltered,accYFiltered, accZFiltered)
accc = normWithoutDC(accNorm,N)

# plt.figure()
# plt.plot(time,accNorm,"r-", time,accc,"b.")
# plt.plot(time,accXFiltered,"r", time,accX,"r", time,
# accYFiltered,"b", time,accY,"b", time,accZ,"g", time,accZFiltered,"g")

okienko(accNorm,100,70)
# plt.show()
