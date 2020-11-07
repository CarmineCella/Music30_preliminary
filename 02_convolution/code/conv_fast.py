import soundfile as sf
import numpy as np
import sys

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

def main():
    print("conv_fast.py - fast convolution based reverberation")
    x, srx = sf.read('anechoic1.wav')
    h, srh = sf.read('Concertgebouw-m.wav')
    print (x.shape)
    print (h.shape)        

    if srx != srh:
        sys.exit('sr must be the same in both files')

    if x.shape[0] > h.shape[0]:
        N = next_power_of_2(x.shape[0])
    else:
        N = next_power_of_2(h.shape[0])            

    scale = .3
    direct = 0

    y = np.fft.irfft (np.fft.rfft (x, N) * np.fft.rfft  (h, N))
    y *= scale
    y[0:x.shape[0]] += x * direct

    print ("saving data")
    sf.write ("outverb.wav", y, srx)
    print ("end")

# main call
main()

