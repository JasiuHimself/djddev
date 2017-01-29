#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
# Hz sa rozpatrywane w przedziale sekundy
# sekunda to ilość próbek razy częstotliwość próbkowania
# 1s = f*i chyba

# Number of sample points
N = 250
# sample spacing
dt=1.0/50.0 #0.02s = 1/50s sampling spacing
Fs = 1/dt #częstotliwość próbkowania


# cały zakres czasowy okna to N*dt [s]
# zakres = N *dt
# print zakres

#GENEROWANIE SINUSA
x = np.linspace(0.0, N*dt, N)

y=np.sin( 2*np.pi*x)
y = np.sin(2.0*np.pi*x)+ 0.1*np.sin(10.0 * 2.0*np.pi*x)+ np.sin(20.0 * 2.0*np.pi*x)+ np.sin(5 * 2.0*np.pi*x)


#FOURIER
yf = np.fft.rfft(y)
yf = abs(yf)
xf = np.fft.rfftfreq(len(y),dt) # FREQUENCIES

# magnitudes = abs(yf[np.where(xf >= 0)])
# # print positive_frequencies
# # print magnitudes
# peak_frequency = np.argmax(magnitudes)
# print peak_frequency
def findPeakFrequencies(xf,yf):
    peaksVector = []
    previousSample = 0
    alreadyAdded = 0
    for i in range(len(yf)):
        if(yf[i]>=previousSample): #rośnie
            alreadyAdded = 0
        else: #maleje
            if (alreadyAdded == 0):
                peaksVector.append(xf[i-1]) # minus jeden bo bierzemy wcześniejszy
                alreadyAdded = 1
        previousSample = yf[i]
    print peaksVector

findPeakFrequencies(xf,yf)




plt.figure()
plt.plot(x,y)
plt.ylabel('wartosc sygnalu')
plt.xlabel('sekundy')
plt.grid(True)

plt.figure()
# plt.plot(xf[0:100],abs(yf)[0:10])
plt.stem(xf,yf)
plt.ylabel('wartosc amplitudy')
plt.xlabel('Hz')
plt.grid(True)
plt.show()
