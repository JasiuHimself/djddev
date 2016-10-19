import string
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

def column(matrix, i):
    return [row[i] for row in matrix]

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

# accY = column(vector,2)
# accZ = column(vector,3)


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


# Filter requirements.
order = 10
fs = 199      # sample rate, Hz
cutoff = 15 # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)


accXFiltered = butter_lowpass_filter(accX,cutoff,fs,order)
plt.plot(time,accXFiltered,"g", time,accX,"r")
plt.plot();



plt.show()
