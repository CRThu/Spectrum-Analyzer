import math
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import mpl
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from scipy import signal as wd
from scipy.fftpack import fft, ifft

import fftwin
import adcmodel

Window = 'blackmanharris'


# Sample Info
N = 1024
fs = 193986.56
FS = 2.5
FS_Vrms = FS / 2 / math.sqrt(2)
Wave = 'sine'
Wave_offset = 0
#Wave_freq = 1001.22
#Wave_freq = 1000.105
Wave_freq = 10000.11

adcout = adcmodel.adcmodel(N=N, fs=fs, FS=FS,
                           HDx=[-20, -30, -40],
                           Wave=Wave, Wave_freq=Wave_freq, Wave_offset=Wave_offset, Wave_Vrms=0.776,
                           adc_bits=None, DR=30)


N = len(adcout)
half_N = int(N / 2) + 1

fft_freq = np.linspace(0, fs / 2, half_N)

# FFT
signal_fft = fft(adcout)
signal_fft = signal_fft[range(half_N)]
fft_mod = np.abs(signal_fft)
fft_phase = np.angle(signal_fft)

# FFT Nomalized : DC & Vamp
fft_mod[0] = fft_mod[0] / N
fft_mod[range(1, half_N)] = fft_mod[range(1, half_N)] * 2 / N

# FFT with window
# Window
# winN = wd.blackmanharris(N)
if fftwin.has_window(Window):
    winN = fftwin.get_window(Window, N)

signal_win = winN * adcout

signal_fft_win = fft(signal_win)
signal_fft_win = signal_fft_win[range(half_N)]
fft_mod_win = np.abs(signal_fft_win)
fft_phase_win = np.angle(signal_fft_win)

# FFT Nomalized : DC & Vamp
fft_mod_win[0] = fft_mod_win[0] / N
fft_mod_win[range(1, half_N)] = fft_mod_win[range(1, half_N)] * 2 / N

plt.figure()
plt.plot(fft_freq / 1e3, fft_mod_win, 'black',
         linewidth=1.5, alpha=0.9, label='FFT with Window')
plt.plot(fft_freq / 1e3, fft_mod, 'red', linewidth=1.5,
         alpha=0.9, label='FFT without Window')
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")
plt.grid(True, which='both')
plt.legend()
plt.title("Frequency-domain signal")
plt.savefig("./image/sig_with_win.png", dpi=600)
