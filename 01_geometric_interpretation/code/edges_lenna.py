from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def main():
    lenna = plt.imread('Lenna.jpg')
    lenna = rgb2gray(lenna)

    print (lenna.shape)
    
    Gx = np.zeros ((3, 3))
    Gy = np.zeros ((3, 3))    
    Gx =  [[1,  2, 1], [0,  0,  0], [-1, -2, -1]]
    Gy = [[1,  0,  -1],  [2, 0, -2],  [1, 0, -1]]

    lennaY = signal.convolve2d (lenna, Gy)
    lennaX = signal.convolve2d (lenna, Gx)

    gradient = np.sqrt(np.square(lennaX) + np.square(lennaY))
    gradient *= 255.0 / gradient.max()
 
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.imshow (Gx)
    plt.subplot(2, 1, 2)
    plt.imshow (Gy)


    plt.figure(2)
    plt.subplot(2, 2, 1)
    plt.imshow (lenna)
    plt.subplot(2, 2, 2)
    plt.imshow (lennaX)
    plt.subplot(2, 2, 3)
    plt.imshow (lennaY)
    plt.subplot(2, 2, 4)
    plt.imshow (gradient)
    plt.show()

# main call
main()
