#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import numpy as np
import csv
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
    for n in range(0,len(signal)):
        sumator += signal[n]
    return (1.0/len(signal))*sumator

def signalVariance(signal):
    sumator = 0
    meanValue = signalEnergy(signal) #signal mean value
    for n in range(0, len(signal)):
        sumator += pow((signal[n] - meanValue),2)
    return (1.0/len(signal))*sumator

def fft(signal):
    return np.fft.fft(signal)

def window(signal,windowWidth, overlappingPercent = 0, currentPositionInSignal = 0):
    overlapping = 0
    if (overlappingPercent):
        overlapping = (int)(overlappingPercent/100.0*windowWidth)
    windowBegining = currentPositionInSignal * windowWidth - currentPositionInSignal * overlapping
    if (windowBegining + windowWidth <= len(signal)):
        window = signal[windowBegining:windowBegining+windowWidth]
        return window #, currentPositionInSignal+1
    else:
        return False

def createTimeVectorToPlotWindow(windowWidth, overlappingPercent, currentPositionInSignal =0):
    overlapping = 0
    if (overlappingPercent):
        overlapping = (int)(overlappingPercent/100.0*windowWidth)
    windowBegining = currentPositionInSignal * windowWidth - currentPositionInSignal * overlapping
    return range(windowBegining,windowBegining+windowWidth)

def signalRangeInWindowsCount(signal, windowWidth, overlappingPercent):
    overlapping = 0
    windowsCount = 0
    windowBegining = 0
    if (overlappingPercent):
        overlapping = (int)(overlappingPercent/100.0*windowWidth)
    while(windowBegining + windowWidth <= len(signal)):
        windowsCount += 1
        windowBegining += windowWidth - overlapping
    return windowsCount

def readDataFile(dataFileName):
    csv_in = open(dataFileName, 'rb')
    myreader = csv.reader(csv_in)

    sample_Class_vector = []
    accX_vector = []
    accY_vector = []
    accZ_vector = []
    gyrR_vector = []
    gyrP_vector = []
    gyrY_vector = []

    for row in myreader:
        sample_Class, accX, accY, accZ, gyrR, gyrP, gyrY = row
        sample_Class_vector, accX_vector, accY_vector, accZ_vector, gyrR_vector, gyrP_vector, gyrY_vector = zip(*myreader)
        accX_vector = map(float, accX_vector)
        accY_vector = map(float, accY_vector)
        accZ_vector = map(float, accZ_vector)
        gyrR_vector = map(float, gyrR_vector)
        gyrP_vector = map(float, gyrP_vector)
        gyrY_vector = map(float, gyrY_vector)

    return sample_Class_vector, accX_vector, accY_vector, accZ_vector, gyrR_vector, gyrP_vector, gyrY_vector



#otworz plik i zapisz wartosc do wektora
sample_Class,accX,accY,accZ,gyrR,gyrP,gyrY = readDataFile('accgyrclass.csv');

windowWidth = 2
overlappingPercent = 0



accNormDC = normWithoutDC(norm(accX,accY,accZ))
gyrNormDC = normWithoutDC(norm(gyrR,gyrP,gyrY))



plt.figure()
plt.subplot(2,1,1)
plt.hold(True)
plt.grid(True)

plt.plot(accNormDC)


# Zaznacznie dzialania okienek
#
# typyPlotu = ['x', 'o', '*', '+', 's', 'd', 'v', '^', '<']
#
# for i in range(0,9):
#     wycinek, pozycja = window(accNormDC,10,50,i)
#     czasik = createTimeVectorToPlotWindow(10,50,i)
#     plt.plot(czasik,wycinek, typyPlotu[i])

# plotowanie energii
# for i in range(0, signalRangeInWindowsCount(accNormDC, windowWidth, overlappingPercent)):
#     energy = signalEnergy(window(accNormDC,windowWidth,overlappingPercent,i))
#     energyWindow = np.empty(windowWidth);
#     energyWindow.fill(energy)
#     plt.plot(createTimeVectorToPlotWindow(windowWidth,overlappingPercent,i),energyWindow,'g-')

# plotowanie wariancji
# for i in range(0, signalRangeInWindowsCount(accNormDC, windowWidth, overlappingPercent)):
#     variance = signalVariance(window(accNormDC,windowWidth,overlappingPercent,i))
#     print variance
#     varianceWindow = np.empty(windowWidth);
#     varianceWindow.fill(variance)
#     plt.plot(createTimeVectorToPlotWindow(windowWidth,overlappingPercent,i),varianceWindow,'r-')

# GYROSCOPE

plt.subplot(2,1,2)
plt.hold(True)

plt.plot(gyrNormDC)

# plotowanie wariancji

plt.show()
