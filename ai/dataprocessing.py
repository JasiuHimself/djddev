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

def norm(vector1, vector2, vector3):
    norm = []
    for i in range(len(vector1)):
         norm.append(math.sqrt(pow(vector1[i],2)+pow(vector2[i],2)+pow(vector3[i],2)))
    return norm

def normWithoutDC(norm):
    normWithoutDC = []
    for n in range(0, len(norm)):
        sumator = 0
        for l in range(0,len(norm)):
            sumator += norm[n-l]
        normWithoutDC.append(norm[n]-((1.0/len(norm))*sumator))
    return normWithoutDC

#aka srednia arytmetyczna
def signalEnergy(signal):
    sumator = 0
    for n in range(0,N):
        print sumator
        sumator += signal[n]
    return (1.0/N)*sumator

def signalVariance(signal):
    sumator = 0
    meanValue = signalEnergy(signal,N) #signal mean value
    for n in range(0, N):
        sumator += pow((signal[n] - meanValue),2)
    return (1.0/N)*sumator


def okienko(signal,windowWidth, overlappingPercent = 0, currentPositionInSignal = 0):
    if (overlappingPercent):
        overlapping = (int)(overlappingPercent/100.0*windowWidth)
    windowBegining = currentPositionInSignal * windowWidth - currentPositionInSignal * overlapping
    if (windowBegining + windowWidth <= len(signal)):
        window = signal[windowBegining:windowBegining+windowWidth]
        return window, currentPositionInSignal+1
    else:
        return False



def createTimeVectorToPlotWindow(windowWidth, overlappingPercent, currentPositionInSignal):
    if (overlappingPercent):
        overlapping = (int)(overlappingPercent/100.0*windowWidth)
    windowBegining = currentPositionInSignal * windowWidth - currentPositionInSignal * overlapping
    return range(windowBegining,windowBegining+windowWidth)



def readDataFile(dataFileName):
    dataFile = open(dataFileName, 'r')
    vector = []
    while True:
        line = dataFile.readline();
        if not line: break
        line = line.rstrip()
        vector.append([float(x) for x in line.split(',')])
    dataFile.close
    return vector





#otworz plik i zapisz wartosc do wektora
vector = readDataFile('accgyr.csv');



#sample_Class = column(vector,0)
accX = column(vector,0)
accY = column(vector,1)
accZ = column(vector,2)
gyrR = column(vector,3)
gyrP = column(vector,4)
gyrY = column(vector,5)
accNorm = norm(accX,accY,accZ)
gyrNorm = norm(gyrR,gyrP,gyrY)
accNormDC = normWithoutDC(accNorm)
gyrNormDC = normWithoutDC(gyrNorm)


plt.figure()

plt.subplot(2,1,1)
plt.hold(True)
plt.grid(True)
plt.plot(accX)
plt.plot(accY)
plt.plot(accZ)
plt.plot(accNorm,'.')
plt.plot(accNormDC,'x')

typyPlotu = ['x', 'o', '*', '+', 's', 'd', 'v', '^', '<']

for i in range(0,9):
    wycinek, pozycja = okienko(accX,10,50,i)
    czasik = createTimeVectorToPlotWindow(10,50,i)
    plt.plot(czasik,wycinek, typyPlotu[i])


# GYROSCOPE

plt.subplot(2,1,2)
plt.hold(True)
plt.plot(gyrR)
plt.plot(gyrP)
plt.plot(gyrY)
plt.plot(gyrNorm,'.')
plt.plot(gyrNormDC,'x')

plt.show()
