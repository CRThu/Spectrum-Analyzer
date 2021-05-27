import math
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import mpl
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from scipy import signal as wd
from scipy.fftpack import fft, ifft


fs = 10000
gen_freq = [0.107, 0.2505, 0.3503]
N = 256

# Time data
# T=1.0 2.0 3.0
t1 = np.arange(0, N, 1)
sig = np.array((1.0 * np.sin(2 * np.pi * gen_freq[0] * t1) +
                0.3 * np.sin(2 * np.pi * gen_freq[1] * t1) +
                0.1 * np.sin(2 * np.pi * gen_freq[2] * t1)))


N = len(sig)
half_N = int(N / 2) + 1

# FFT
signal_fft = fft(sig)
signal_fft = signal_fft[range(half_N)]

fft_freq = np.linspace(0, fs / 2, half_N)

fft_mod = np.abs(signal_fft)
fft_phase = np.angle(signal_fft)

# FFT Nomalized : DC & Vamp
fft_mod[0] = fft_mod[0] / N
fft_mod[range(1, half_N)] = fft_mod[range(1, half_N)] * 2 / N

plt.figure()
plt.plot(t1/fs * 1e3, sig, 'b', label='Time')
plt.xlabel("Time (ms)")
plt.ylabel("Magnitude")
plt.grid(True, which='both')
plt.legend()
plt.title("Time-domain signal")
plt.savefig("./image/sig_time.png", dpi=600)

plt.figure()
plt.plot(fft_freq / 1e3, fft_mod, 'b', label='FFT')
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")
plt.grid(True, which='both')
plt.legend()
plt.title("Frequency-domain signal")
plt.savefig("./image/sig_freq.png", dpi=600)

