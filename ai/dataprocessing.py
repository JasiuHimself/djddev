import string
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
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
        for l in range(0,N-1):
            sumator = norm[n-l]
        normWithoutDC.append(norm[n]-((1.0/N)*sumator))
    return normWithoutDC




# chce 2.5 sekundy f=200 wiec biere n=500
N = 500
# Filter requirements.
order = 10
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
def butter_lowpass(cutoff, fs, order=5):
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

# plt.plot(time,accXFiltered,"r", time,accX,"r",
# time, accYFiltered,"b", time,accY,"b",
# time,accZFiltered,"g",
plt.plot(time,accNorm,"r-", time,accc,"b.")
plt.show()
