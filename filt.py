import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#b, a = signal.butter(4, 100, 'low', analog=True)
#w, h = signal.freqs(b, a)

w = np.linspace(1e-8, math.pi, 65536)
H = np.ones(len(w))
H *= np.sin(w * 6 / 2) / np.sin(w / 2)
H *= np.sin(w * 6 / 2) / np.sin(w / 2)
H *= np.sin(w * 5 / 2) / np.sin(w / 2)

H_dB = 20 * np.log10(abs(H))
H_dB -= np.max(H_dB)

#plt.semilogx(w, 20 * np.log10(abs(H)))
plt.plot(w/  math.pi, H_dB)
plt.title('Filter frequency response')
plt.xlabel('Frequency [radians / second]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.ylim(top = 1, bottom = -120)
plt.grid(which='both', axis='both')
#plt.axvline(100, color='green') # cutoff frequency
xmajorLocator = MultipleLocator(0.05 * math.pi)
xmajorFormatter = FormatStrFormatter('%5.2f π')
plt.gca().xaxis.set_major_locator(xmajorLocator)
plt.gca().xaxis.set_major_formatter(xmajorFormatter)
plt.show()