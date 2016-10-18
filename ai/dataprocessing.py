import string
from scipy import signal
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
accXFiltered = accX
# accY = column(vector,2)
# accZ = column(vector,3)


b, a = signal.butter(4, 100, 'low', analog=True)
w, h = signal.freqs(b, a)
plt.plot(w, 20 * np.log10(abs(h)))

plt.plot(time, accX);





plt.show()
