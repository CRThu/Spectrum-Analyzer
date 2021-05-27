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
import analysis_util as util

Window = 'blackmanharris'
#Window = ['rectangle','blackmanharris','HFT90D']

# Sample Info
N = 1024
fs = 200000
FS = 2.5
FS_Vamp = FS / 2
FS_Vrms = FS / 2 / math.sqrt(2)
Wave = 'sine'
Wave_offset = 0
Wave_freq = 9570.3125 * 3

adcout = adcmodel.adcmodel(N=N, fs=fs, FS=FS,
                           #HDx=[-45, -60, -75],
                           Wave=Wave, Wave_freq=Wave_freq, Wave_offset=Wave_offset, Wave_Vrms=0.776,
                           adc_bits=None, DR=None)


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

# Nomalized : FS
fft_mod = fft_mod / FS_Vamp
fft_mod_win = fft_mod_win / FS_Vamp
# Nomalized : dB
fft_mod = util.vratio2db_np(fft_mod)
fft_mod_win = util.vratio2db_np(fft_mod_win)

plt.figure()
plt.plot(fft_freq / 1e3, fft_mod_win, 'black',
         linewidth=1.5, alpha=0.9, label='FFT with Blackman-Harris Window')
plt.plot(fft_freq / 1e3, fft_mod, 'red', linewidth=1.5,
         alpha=0.9, label='FFT without Window')
plt.ylim(top=1, bottom=-200)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude(dBFS)")
plt.grid(True, which='both')
plt.legend()
plt.title("Frequency-domain signal")
plt.savefig("./image/sig_with_window_compare.png", dpi=600)
