
from threading import Thread
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt

def show():
    plt.grid(True, which = 'both')
    plt.plot([1,2,3,4,5], [10,20,30,40,50])
    plt.show()

thread1 = Thread(target=show)

thread1.start()