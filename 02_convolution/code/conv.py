import soundfile as sf
import numpy as np
import sys

def main():
    print("conv.py - convolution based reverberation")
    x, srx = sf.read('anechoic1.wav')
    h, srh = sf.read('Concertgebouw-m.wav')
    print (x.shape)
    print (h.shape)    

    if srx != srh:
        sys.exit('sr must be the same in both files')

    scale = 0.1
    direct = 0.7
    y = np.ndarray ((x.shape[0] + h.shape[0],))
    print ("computing reverb")
    for t in range(x.shape[0]):
        for m in range(h.shape[0]):
            y[t + m] = y[t + m] + x[t] * h[m] * scale
        y[t] = y[t] + x[t] * direct
        if (t % 100 == 0):
            print (t)
    print ("saving data")
    sf.write ("outverb.wav", y, srx)
    print ("end")

# main call
main()

