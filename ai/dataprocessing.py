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

class Dataset:
    def __init__(self, dataFileName, windowWidth, overlappingPercent):
        self.dataFileName = dataFileName
        self.windowWidth = windowWidth
        self.overlapping = self.overlappingCount(windowWidth,overlappingPercent )
        self.readDataFile(self.dataFileName)
        self.accNormDC = self.normWithoutDC(self.norm(self.accX,self.accY,self.accZ))
        self.gyrNormDC = self.normWithoutDC(self.norm(self.gyrR,self.gyrP,self.gyrY))
        self.currentPositionInSignal = 0
        self.classesPositionsAndWindowsCounts = []
        # self.calculateClassesPositionsAndWindowsConunts()
        self.returnWindowsCountAndNewClassBeginning(0)


    def readDataFile(self,dataFileName):
        csv_in = open(dataFileName, 'rb')
        myreader = csv.reader(csv_in)

        class_vector = []
        accX = []
        accY = []
        accZ = []
        gyrR = []
        gyrP = []
        gyrY = []
        self.class_vector, accX, accY, accZ, gyrR, gyrP, gyrY = zip(*myreader)
        self.accX = map(float, accX)
        self.accY = map(float, accY)
        self.accZ = map(float, accZ)
        self.gyrR = map(float, gyrR)
        self.gyrP = map(float, gyrP)
        self.gyrY = map(float, gyrY)


    def norm(self,vector1, vector2, vector3):
        norm = []
        for i in range(len(vector1)):
             norm.append(math.sqrt(pow(vector1[i],2)+pow(vector2[i],2)+pow(vector3[i],2)))
        return norm

    def normWithoutDC(self,norm):
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

    def window(self,signal, currentPositionInSignal = 0):
        windowBeginning = currentPositionInSignal #* windowWidth - currentPositionInSignal * overlapping
        if (windowBeginning + self.windowWidth <= len(signal)):
            window = signal[windowBeginning:windowBeginning+self.windowWidth]
            return window
        else:
            return False

    def iterateThroughWindows(self, currentClass):
        classBeginning, windowsCount = self.classesPositionsAndWindowsCounts[currentClass]
        print "classBeginning: "+str(classBeginning)+ " windowsCount: " + str(windowsCount)
        for currentWindow in range(windowsCount):
            print self.window(self.class_vector, classBeginning+currentWindow*self.windowWidth - self.overlapping * currentWindow)


    def overlappingCount(self,windowWidth, overlappingPercent = 0 ):
        overlapping = 0
        if (overlappingPercent):
            overlapping = (int)(overlappingPercent/100.0*windowWidth)
        return overlapping

    def createTimeVectorToPlotWindow(windowWidth, overlappingPercent, currentPositionInSignal =0):
        overlapping = overlappingCount(windowWidth, overlappingPercent)
        windowBeginning = currentPositionInSignal * windowWidth - currentPositionInSignal * overlapping
        return range(windowBeginning,windowBeginning+windowWidth)

    def signalRangeInWindowsCount(signal, windowWidth, overlappingPercent):
        overlapping = overlappingCount(windowWidth, overlappingPercent)
        windowsCount = 0
        windowBeginning = 0
        while(windowBeginning + windowWidth <= len(signal)):
            windowsCount += 1
            windowBeginning += windowWidth - overlapping
        return windowsCount


#
#
# Zapisuję postęp
#     def returnWindowsCountAndNewClassBeginning(self, windowBeginning = 0):
#         nextClassBeginning = 0
#         windowCount = 0    # NIE TYKAĆ TEGO WARUNKU - JEST DOBRY (WHILE PONIŻEJ)
#         while (windowBeginning + self.windowWidth-1 <= len(self.class_vector)-1):#przesuniecie indeksu do zera
#             consistent = True
#             # sprawdz czy zawartosc kolejnego okna nalezy do jednej klasy
#             for i in range (windowBeginning+1, windowBeginning+self.windowWidth): #bo nie porownujemy tego samego elementu
#                 if (self.class_vector[i] != self.class_vector[windowBeginning]):
#                     consistent = False
#                     print "inc " + str(windowBeginning) + " : " + self.class_vector[windowBeginning]   + " "+ str(i) + " : "  + self.class_vector[i]
#                 else:
#                     print "con " + str(windowBeginning) + " : " + self.class_vector[windowBeginning] +" " + str(i) + " : "  + self.class_vector[i]
#             windowBeginning +=  self.windowWidth - self.overlapping
#







    def returnWindowsCountAndNewClassBeginning(self, windowBeginning = 0):
        windowsCount = 0    # NIE TYKAĆ TEGO WARUNKU - JEST DOBRY (WHILE PONIŻEJ)
        while (windowBeginning + self.windowWidth-1 <= len(self.class_vector)-1):#przesuniecie indeksu do zera
            consistent = True
            # sprawdz czy zawartosc kolejnego okna nalezy do jednej klasy
            for i in range (windowBeginning+1, windowBeginning+self.windowWidth): #bo nie porownujemy tego samego elementu
                if (self.class_vector[i] != self.class_vector[windowBeginning]):
                    consistent = False

            if (consistent):
                windowBeginning +=  self.windowWidth - self.overlapping
                windowsCount+=1
            else:
                newClassBeginning = windowBeginning+1
                while(self.class_vector[windowBeginning]==self.class_vector[newClassBeginning]):
                    print newClassBeginning
                    newClassBeginning+=1
                break
        # print "pierwszy element nowe klasy: " + str(newClassBeginning) + 'to' + self.class_vector[newClassBeginning] + "ilosc okien:" + str(windowCount)
        return windowCounts, newClassBeginning





    def calculateClassesPositionsAndWindowsConunts(self):
        thereIsNextClass = True
        windowBeginning = 0
        newClassBeginning = 0
        oldClassBeginnig = 0
        while(thereIsNextClass):
            windowsCount,newClassBeginning = self.returnWindowsCountAndNewClassBeginning(oldClassBeginnig)
            self.classesPositionsAndWindowsCounts.append((oldClassBeginnig,windowsCount))
            oldClassBeginnig = newClassBeginning
            if not(newClassBeginning):
                thereIsNextClass = False
        print self.classesPositionsAndWindowsCounts

        # iterowanie przez wszystkie klasy
        for classIterator in range (len(self.classesPositionsAndWindowsCounts)):
            self.iterateThroughWindows(classIterator)



# nazwa pliku, szerokosc okna(CO NAJMNIEJ 2), overlapping
dataset = Dataset('accgyrclass.csv',4,50)


#
#
# plt.figure()
# plt.subplot(2,1,1)
# plt.hold(True)
# plt.grid(True)
#
# plt.plot(accNormDC)


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

# plt.subplot(2,1,2)
# plt.hold(True)
# plt.plot(gyrNormDC)



# plt.show()
