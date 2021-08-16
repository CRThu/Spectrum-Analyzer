import numpy as np
from scipy import signal
from scipy.fftpack import fft,fftshift
import matplotlib.pyplot as plt
import fftwin

#window = signal.windows.blackmanharris(256)
#window = signal.windows.kaiser(51, beta=100)
#window = fftwin.get_window('HFT248D', 256)
window = fftwin.get_window('blackmanharris', 256)
plt.plot(window)
plt.title(r"window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")

plt.figure()
A = fft(window, 256) / (len(window)/2.0)
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
plt.plot(freq, response, linewidth = 1, marker = '.', markersize = 3)
#plt.axis([-0.5, 0.5, -120, 0])
plt.axis([-0.2, 0.2, -400, 1])
plt.title(r"Frequency response of the window")
plt.ylabel("Normalized magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")
plt.show()