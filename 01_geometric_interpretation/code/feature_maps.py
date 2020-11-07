from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

import soundfile as sf

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def main():
    x, srx = sf.read('fake_mixture.wav')
    
    f, t, Sxx = signal.spectrogram(x, srx, nfft=4096)
    Sxx =abs (Sxx[0:1024, :])
    plt.figure(1)
    plt.imshow(np.log (0.0000001 + Sxx), aspect='auto', cmap='plasma', origin='lower')
    plt.tight_layout()
    # plt.show ()
    
    kernel_size = 25
    blur_size = 3

    gliss_down = np.eye (kernel_size)
    gliss_down = signal.convolve2d(gliss_down, np.random.random((blur_size, blur_size)))
    gliss_up = np.flipud (gliss_down)
    gliss_up = signal.convolve2d(gliss_up, np.random.random((blur_size, blur_size)))
    steady = np.zeros((kernel_size, kernel_size))
    steady[round(kernel_size/2),:] = 1
    steady = signal.convolve2d(steady, np.random.random((blur_size, blur_size)))
    impulse = np.zeros((kernel_size, kernel_size))
    impulse[:,round(kernel_size/2)] = 1
    impulse = signal.convolve2d(impulse, np.random.random((blur_size, blur_size)))
    
    plt.figure(2)
    plt.subplot(2, 2, 1)
    plt.imshow (gliss_down)
    plt.title ('Down')
    plt.subplot(2, 2, 2)
    plt.imshow (gliss_up)
    plt.title ('Up')
    plt.subplot(2, 2, 3)
    plt.imshow (steady)
    plt.title ('Steady')
    plt.subplot(2, 2, 4)
    plt.imshow (impulse)
    plt.title ('Impulse')
    plt.tight_layout()

    # threshold = .7
    glissdn_map =( np.log (.0000001 + signal.convolve2d (Sxx, gliss_down)))
    # glissdn_map[glissdn_map > glissdn_map.max() * threshold] = 0
    glissup_map = (np.log (.0000001 + signal.convolve2d (Sxx, gliss_up)))
    # glissup_map[glissup_map > glissup_map.max() * threshold] = 0
    steady_map =  (np.log (.0000001 + signal.convolve2d (Sxx, steady)))
    # steady_map[steady_map > steady_map.max() * threshold] = 0
    impulse_map =  (np.log (.0000001 + signal.convolve2d (Sxx, impulse)))
    # impulse_map[impulse_map > impulse_map.max() * threshold] = 0
    
    plt.figure(3)
    plt.subplot(2, 2, 1)
    plt.imshow (glissdn_map)
    plt.title ('MAP Down')
    plt.subplot(2, 2, 2)
    plt.imshow (glissup_map)
    plt.title ('MAP Up')
    plt.subplot(2, 2, 3)
    plt.imshow (steady_map)
    plt.title ('MAP Steady')
    plt.subplot(2, 2, 4)
    plt.imshow (impulse_map)
    plt.title ('MAP Impulse')
    plt.tight_layout()

    plt.show()

# main call
main()


