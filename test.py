import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from scipy import signal as wd
import math
import fftwin
import adcmodel
import analysis_util as util


Wave_offset = 0
Wave_freq = 1333
N = 8192
fs = 20000
FS = 2.5
amp_ratio = 0.99
FS_Vrms = FS / 2 / math.sqrt(2)
adc_bits = 8

dc = Wave_offset
fsin_base = Wave_freq
fsin = [fsin_base]
Vrms = [amp_ratio * FS_Vrms]
phase = [0]

t = np.linspace(0, N/fs, N)

sinout = util.vrms2amp(Vrms[0]) * np.sin(2 * np.pi * fsin[0] * t + phase[0])

if adc_bits is not None:
    lsb = FS / (2 ** adc_bits)
    sinout = np.round(sinout / lsb) * lsb

sinout -= np.mean(sinout)
adcout = sinout

signal_k = np.arange(N)
winN = wd.blackmanharris(N)
N = len(adcout)
half_N = int(N / 2) + 1

signal_win = winN * adcout

# FFT
signal_fft = fft(signal_win)
signal_fft = signal_fft[range(half_N)]

fft_freq = np.linspace(0, fs / 2, half_N)

fft_mod = np.abs(signal_fft)
fft_phase = np.angle(signal_fft)

# dBFS Calc
fft_mod_dbfs = np.zeros(half_N)

# Nomalized : dB
fft_mod_dbfs = util.vratio2db_np(fft_mod)

plt.figure('Amplitude Spectrum', figsize = (8, 5))
plt.title('Amplitude Spectrum')
plt.xlabel('Frequency')
plt.ylabel('dbfs')
plt.grid(True, which = 'both')
#plt.plot(fft_freq, fft_mod_dbfs, linewidth = 1, marker = '.', markersize = 3)
plt.plot(fft_freq, fft_mod_dbfs, linewidth = 1, alpha = 0.9, zorder = 100)

plt.show()