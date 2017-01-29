#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import numpy as np
import csv
from math import pi
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
        # to powninno być w oknie przesuwnym
        self.accNorm = self.norm(self.accX,self.accY,self.accZ)
        self.gyrNorm = self.norm(self.gyrR,self.gyrP,self.gyrY)
        self.currentPositionInSignal = 0
        self.classesPositionsAndWindowsCounts = []
        self.calculateClassesPositionsAndWindowsConunts()
        self.accData = []
        self.gyrData = []
        # self.generateDataset()


        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        data = self.accNorm[0:300]

        dt = 0.02
        fourier = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data),dt)
        positive_frequencies = frequencies[np.where(frequencies >= 0)]
        magnitudes = abs(fourier[np.where(frequencies >= 0)])
        print positive_frequencies
        print magnitudes
        peak_frequency = np.argmax(magnitudes)
        print peak_frequency
        plt.plot(magnitudes)
        plt.show()








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
    def signalEnergy(self,signal):
        sumator = 0
        for n in range(len(signal)):
            sumator += signal[n]
        return (1.0/len(signal))*sumator

    def signalStandardDeviation(self,signal):
        return math.sqrt(self.signalVariance(signal))

    def signalVariance(self,signal):
        sumator = 0
        meanValue = self.signalEnergy(signal) #signal mean value
        for n in range(0, len(signal)):
            sumator += pow((signal[n] - meanValue),2)
        return (1.0/len(signal))*sumator

    def fft(self,signal):
        return np.fft.fft(signal)

    def signalSkewness(self,signal):
        sumator = 0
        standardDeviation = self.signalStandardDeviation(signal)
        mean = self.signalEnergy(signal)# meanValue
        for i in range(len(signal)):
            sumator += pow(signal[i] - mean,3)
        if (standardDeviation == 0):
            return 0
        else:
            return sumator/(len(signal)*pow(standardDeviation,3))

    def signalKurtosis(self, signal):
        sumator = 0
        standardDeviation = self.signalStandardDeviation(signal)
        mean = self.signalEnergy(signal)# meanValue
        for i in range(len(signal)):
            sumator += pow(signal[i] - mean,4)
        if (standardDeviation == 0):
            return 0
        else:
            return sumator/(len(signal)*pow(standardDeviation,4))

    def signalFrequencies(self,signal):
        dt = 0.02# inter-sample time difference which is 20ms
        fourier = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal), dt)
        positive_frequencies = frequencies[np.where(frequencies >= 0)]
        magnitudes = abs(fourier[np.where(frequencies >= 0)])  # magnitude spectrum

        frequenciesVector = []
        for i in range(3):
            peak_frequency = np.argmax(magnitudes)
            magnitudes[np.argmax(magnitudes)]=0
            frequenciesVector.append(peak_frequency)
        return frequenciesVector



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



    def returnWindowsCountAndNewClassBeginning(self, windowBeginning = 0):
        windowsCount = 0    # NIE TYKAĆ TEGO WARUNKU - JEST DOBRY (WHILE PONIŻEJ)
        newClassBeginning =0
        while (windowBeginning + self.windowWidth-1 <= len(self.class_vector)-1):#przesuniecie indeksu do zera
            consistent = True
            # sprawdz czy zawartosc okna nalezy do jednej klasy
            for i in range (windowBeginning+1, windowBeginning+self.windowWidth): #bo nie porownujemy tego samego elementu
                if (self.class_vector[i] != self.class_vector[windowBeginning]):
                    consistent = False
            if (consistent):
                windowBeginning +=  self.windowWidth - self.overlapping
                windowsCount+=1

                # jeżeli początek nasępnego okna nie jest poza wektorem klas
                if (windowBeginning<=len(self.class_vector)-1):
                    #jezeli pierwszy element nastepnego okna ma inna klase niz ktorakolwiek probka poprzedniego (consistent)
                    if (self.class_vector[windowBeginning] != self.class_vector[windowBeginning-1] ):
                        newClassBeginning = windowBeginning
                        break
            else:
                newClassBeginning = windowBeginning+1
                while(self.class_vector[windowBeginning]==self.class_vector[newClassBeginning]):
                    # print newClassBeginning
                    newClassBeginning+=1
                break

        # print "pierwszy element nowe klasy: " + str(newClassBeginning) + 'to' + self.class_vector[newClassBeginning] + "ilosc okien:" + str(windowCount)
        return windowsCount, newClassBeginning



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
        # print self.classesPositionsAndWindowsCounts

        # iterowanie przez wszystkie klasy

        # for classIterator in range (len(self.classesPositionsAndWindowsCounts)):
        #      self.iterateThroughWindows(classIterator)



# classBeginning, windowsCount
    def generateDataset(self):
        # print self.classesPositionsAndWindowsCounts
        #dla każdej zbalezionej sekwencji okien
        # csv_out = open('generatedDataset.csv', 'wb')
        csv_out = open('generatedDataset.csv', 'a')

        fileWriter = csv.writer(csv_out, delimiter = ',')
        for i in range (len(self.classesPositionsAndWindowsCounts)):
            # print self.classesPositionsAndWindowsCounts[i]
            # dla każdego okna z danej sekwencji
            windowBeginning  = self.classesPositionsAndWindowsCounts[i][0]
            for j in range(self.classesPositionsAndWindowsCounts[i][1]):
                # TWORZENIE WEKTORÓW GYR I ACC
                currentAccWindow = self.normWithoutDC(self.window(self.accNorm, windowBeginning))
                # currentAccWindow = self.window(self.accNorm, windowBeginning)
                currentGyrWindow = self.normWithoutDC(self.window(self.gyrNorm, windowBeginning))
                # ACC
                currentAccWindowEnergy = abs(self.signalEnergy(currentAccWindow))*100000000000000
                currentAccWindowStandardDeviation = self.signalStandardDeviation(currentAccWindow)
                currentAccWindowVariance = self.signalVariance(currentAccWindow)
                currentAccWindowSkewness = self.signalSkewness(currentAccWindow)
                currentAccWindowKurtosis  = self.signalKurtosis(currentAccWindow)
                currentAccWindowFrequencies = self.signalFrequencies(currentAccWindow)
                # GYR
                currentGyrWindowEnergy = abs(self.signalEnergy(currentGyrWindow))*100000000000000
                currentGyrWindowStandardDeviation = self.signalStandardDeviation(currentGyrWindow)
                currentGyrWindowVariance = self.signalVariance(currentGyrWindow)
                currentGyrWindowSkewness = self.signalSkewness(currentGyrWindow)
                currentGyrWindowKurtosis  = self.signalKurtosis(currentGyrWindow)
                currentGyrWindowFrequencies = self.signalFrequencies(currentGyrWindow)



                # print "okno            " + str(currentAccWindow) + "/okno"
                # print "energy " + str(currentAccWindowEnergy)+" "+  str(currentAccWindowFrequencies)

                currentRow = []
                currentRow.append(self.class_vector[windowBeginning])
                # ACC
                currentRow.append(currentAccWindowEnergy)
                currentRow.append(currentAccWindowStandardDeviation)
                currentRow.append(currentAccWindowVariance)
                currentRow.append(currentAccWindowSkewness)
                currentRow.append(currentAccWindowKurtosis)
                for u in range(len(currentAccWindowFrequencies)):
                    currentRow.append(currentAccWindowFrequencies[u])

                # GYR
                currentRow.append(currentGyrWindowEnergy)
                currentRow.append(currentGyrWindowStandardDeviation)
                currentRow.append(currentGyrWindowVariance)
                currentRow.append(currentGyrWindowSkewness)
                currentRow.append(currentGyrWindowKurtosis)
                for u in range(len(currentGyrWindowFrequencies)):
                    currentRow.append(currentGyrWindowFrequencies[u])

                fileWriter.writerow(currentRow)
                windowBeginning += self.windowWidth - self.overlapping
                # print "......................................................................."





# nazwa pliku, szerokosc okna(CO NAJMNIEJ 2), overlapping
# dataset = Dataset('nicimachanie.csv',250,0)
windowWidth = 250
overlapping = 0
dataset = Dataset('data/BUS1.csv',windowWidth,overlapping)








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
