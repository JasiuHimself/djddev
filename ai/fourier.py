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

N=1000 # number of samples
F=10 # frequency
dt = 0.02# where 0.005 is the inter-sample time difference
t = [i*1./N for i in range(N)]
y = np.sin(2*pi*np.array(t)*F)+np.sin(4*pi*np.array(t)*F)+np.sin(8*pi*np.array(t)*F)

fourier = np.fft.fft(y)
frequencies = np.fft.fftfreq(len(t))
positive_frequencies = frequencies[np.where(frequencies >= 0)]
magnitudes = abs(fourier[np.where(frequencies >= 0)])  # magnitude spectrum


for i in range(4):
    peak_frequency = np.argmax(magnitudes)
    # magnitudes[np.argmax(magnitudes)]=0.00000000001
    # magnitudes[np.argmax(magnitudes)]=0.0000001

    # print peak_frequency
#
# print magnitudes
# print frequencies
print frequencies
print frequencies[np.where(frequencies >= 0)]

print np.fft.fftfreq(10)

# plt.plot(magnitudes)
#
# plt.show()
