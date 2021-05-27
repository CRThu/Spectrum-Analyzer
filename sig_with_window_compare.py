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

Windows = ['rectangle', 'hamming', 'hanning',
           'flattop', 'blackmanharris', 'nuttall3', 'nuttall4']
image_num = 1

#Windows = ['rectangle', 'flattop', 'HFT90D', 'HFT248D']
#image_num = 2

# Sample Info
N = 256
fs = 200000
FS = 2.5
FS_Vamp = FS / 2
FS_Vrms = FS / 2 / math.sqrt(2)
Wave = 'sine'
Wave_offset = 0
Wave_freq = 57 * fs / N

display_range = (10000, 90000)
fft_display_start_bin = math.floor(display_range[0] / fs * N)
fft_display_stop_bin = math.ceil(display_range[1] / fs * N)

adcout = adcmodel.adcmodel(N=N, fs=fs, FS=FS,
                           #HDx=[-45, -60, -75],
                           Wave=Wave, Wave_freq=Wave_freq, Wave_offset=Wave_offset, Wave_Vrms=0.776,
                           adc_bits=None, DR=None)


N = len(adcout)
half_N = int(N / 2) + 1

fft_freq = np.linspace(0, fs / 2, half_N)

plt.figure()
for win in Windows:
    # FFT with window
    if fftwin.has_window(win):
        winN = fftwin.get_window(win, N)
    else:
        winN = wd.get_window(win, N)

    signal_win = winN * adcout

    signal_fft_win = fft(signal_win)
    signal_fft_win = signal_fft_win[range(half_N)]
    fft_mod_win = np.abs(signal_fft_win)
    fft_phase_win = np.angle(signal_fft_win)

    # FFT Nomalized : DC & Vamp
    fft_mod_win[0] = fft_mod_win[0] / N
    fft_mod_win[range(1, half_N)] = fft_mod_win[range(1, half_N)] * 2 / N

    # Nomalized : 0dB
    fft_mod_win = fft_mod_win / np.max(fft_mod_win)
    # Nomalized : dB
    fft_mod_win = util.vratio2db_np(fft_mod_win)

    plt.step(fft_freq[fft_display_start_bin:fft_display_stop_bin] / 1e3,
             fft_mod_win[fft_display_start_bin:fft_display_stop_bin],
             linewidth=1, alpha=0.9, label=win, where='mid')

plt.grid(True, which='both')
#plt.ylim(top=1, bottom=-300)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude(dB Nomalized)")
plt.grid(True, which='both')
plt.legend(loc='upper right')
plt.title("Frequency-domain signal")
plt.savefig("./image/sig_with_window_compare_" +
            str(image_num) + ".png", dpi=600)
