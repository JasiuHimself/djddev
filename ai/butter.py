
# chce 2.5 sekundy f=200 wiec biere n=500
# wielkość okna analizy
N = 500
# Filter requirements.
order = 10  # rzad order
fs = 199      # sample rate, Hz
cutoff = 15 # desired cutoff frequency of the filter, Hz
# Get the filter coefficients so we can check its frequency response.

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
