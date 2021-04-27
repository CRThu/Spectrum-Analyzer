import numpy as np
from scipy import signal
from scipy.fftpack import fft,fftshift
import matplotlib.pyplot as plt
import fftwin

window = signal.windows.blackmanharris(1048576)
#window = signal.windows.kaiser(51, beta=100)
#window = fftwin.get_windows('HFT90D', 1048576)
plt.plot(window)
plt.title(r"window")
plt.ylabel("Amplitude")
plt.xlabel("Sample")

plt.figure()
A = fft(window, 1048576) / (len(window)/2.0)
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
plt.plot(freq, response)
#plt.axis([-0.5, 0.5, -120, 0])
plt.axis([-0.2, 0.2, -400, 1])
plt.title(r"Frequency response of the window")
plt.ylabel("Normalized magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")
plt.show()