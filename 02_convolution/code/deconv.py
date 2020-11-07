import soundfile as sf
import numpy as np
import sys

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

def main():
    print("conv.py - convolution based reverberation")
    y, syx = sf.read('outverb.wav')
    x, srx = sf.read('anechoic1.wav')
    # y, syx = sf.read('pedrotti_dump.wav')
    # x, srx = sf.read('sweep.aif')
    # x, srx = sf.read('Concertgebouw-m.wav')
    print (x.shape)
    # print (h.shape)    
    print (y.shape)

    scale = 3

    N = next_power_of_2(y.shape[0])   
    ft_y = np.fft.fft (y, N)
    ft_x = np.fft.fft (x, N)
    # v =  max(abs(ft_x)) * 0.000005
    v =  max(abs(ft_x)) * 0.005

    print ("deconvolving")
    # resynthesis
    ir_rebuild = np.fft.irfft(ft_y * np.conj (ft_x) / (v + abs (ft_x) ** 2))

    sig_len = y.shape[0] - x.shape[0]
    ir_rebuild = ir_rebuild[1:sig_len] * scale

    print ("saving data")
    sf.write ("ir_rebuild.wav", ir_rebuild, srx)

    print ("end")

# main call
main()


