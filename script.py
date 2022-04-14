import glob
from scipy.io import wavfile
import numpy as np
import warnings
import sys
from scipy.signal import decimate
warnings.filterwarnings("ignore")

def do_hps(signal, r):
    window = np.kaiser(np.size(signal),5)
    signal = signal * window
    fft = np.abs(np.fft.fft(signal)) / r
    fft2 = np.copy(fft)
    for i in range(2,5):
        dec = decimate(fft, int(i))
        fft2[:np.size(dec)] *= dec
    return fft2

def is_male(r, signal):
    Time = min(np.size(signal) / r, 3)
    min_arg = max(0, int(np.size(signal)/2) - int(Time/2*r))
    max_arg = min(np.size(signal) - 1, int(np.size(signal)/2) + int(Time/2*r))
    signal = signal[min_arg:max_arg]
    segment_len = int(r)
    segments = [signal[segment_len*i:segment_len*(i+1)] for i in range(int(Time))]
    
    hpsList = []
    for segment in segments:
        if len(segment) != 0:
            hpsList.append(do_hps(segment, r))
            
    finalList = np.zeros(np.size(hpsList[int(len(hpsList)/2)]))
    for hps in hpsList:
        if np.size(hps) == np.size(finalList): 
            finalList += hps

    return np.sum(finalList[180:270]) < np.sum(finalList[60:160])


if __name__ == "__main__":
    result = 0
    print(sys.argv[0])
    files = glob.glob("input/*.wav")
    for file in files:
        rate, array = wavfile.read(file)
        if np.size(array[0]) == 2:
            array = [s[1] for s in array]
        found = is_male(rate, array)
        if found == 1:
            if file[-5:-4] == 'M':
                result += 1
        else:
            if file[-5:-4] == 'K':
                result += 1
    print(f"ACCURACY: {result / len(files)}")
    #ACCURACY: 0.967032967032967