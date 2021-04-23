import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from scipy import signal as wd
import math
import fftwin
import adcmodel
import analysis_util

info = {
    'name' : 'FFT ANALYSIS PROGRAM',
    'project' : '202116A',
    'version' : '0.0.1',
    'release' : 'alpha',
    'author' : 'written by carrot',
}

def fftplot(signal, fs, fbase,
    Wave = 'Raw',
    Zoom = 'All', Zoom_fin = -1, Zoom_period = 3,
    Nomalized = 'dBFS', FS = -1,
    Window = 'HFT248D'):
    
    #TODO Fix Bugs in Vrms
    assert Nomalized != 'Vrms'

    # FFT
    N = len(signal)
    half_N = int(N / 2) + 1

    signal_k = np.arange(N)

    # Window
    CPG = -1    # dB
    if Window == 'Raw':
        winN = np.ones(N)
        CPG = 0.000
    elif Window == 'rectangle':
        winN = np.ones(N)
        CPG = 0.000
    elif Window == 'blackmanharris':
        winN = wd.windows.blackmanharris(N)
        CPG = 8.904
    elif Window == 'flattop':
        winN = wd.windows.flattop(N)
        CPG = 13.328
    elif Window == 'HFT90D':
        winN = fftwin.HFT90D(N)
        CPG = 0.000
    elif Window == 'HFT144D':
        winN = fftwin.HFT144D(N)
        CPG = 0.000
    elif Window == 'HFT248D':
        winN = fftwin.HFT248D(N)
        CPG = 0.000
    assert CPG >= 0

    signal_win = winN * signal
    signal_win_amp_cal = math.pow(10, CPG / 20) * signal_win

    fft_signal_amp_cal = fft(signal_win_amp_cal)
    fft_signal_amp_cal = fft_signal_amp_cal[range(half_N)]

    #fft_k = np.arange(half_N)
    fft_freq = np.linspace(0, fs / 2, half_N)

    fft_mod_amp_cal = np.abs(fft_signal_amp_cal)
    fft_phase_amp_cal = np.angle(fft_signal_amp_cal)

    # FFT Nomalized : DC & Vamp
    fft_mod_amp_cal[0] = fft_mod_amp_cal[0] / N
    fft_mod_amp_cal[range(1,half_N)] = fft_mod_amp_cal[range(1,half_N)] * 2 / N

    if Nomalized == 'dBFS':
        assert FS > 0
        # Nomalized : FS
        fft_mod_amp_cal[0] = fft_mod_amp_cal[0] / FS
        fft_mod_amp_cal[range(1,half_N)] = fft_mod_amp_cal[range(1,half_N)] * 2 / FS
        # Nomalized : dB
        fft_mod_amp_cal = 20 * np.log10(fft_mod_amp_cal)
    elif Nomalized == 'Vrms':
        # Nomalized : Vrms
        fft_mod_amp_cal[range(1,half_N)] = fft_mod_amp_cal[range(1,half_N)] * 2 

    # Config
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'

    # Time Domain Plot
    plt.figure('Time', figsize = (8, 5))
    plt.title('Time')
    plt.xlabel('Samples')
    plt.ylabel('Voltage')
    plt.grid(True, which = 'both')
    if Zoom == 'All':
        if Wave == 'Raw':
            #plt.plot(signal_k, signal, linewidth = 1, marker = '.', markersize = 3)
            plt.plot(signal_k, signal, linewidth = 1)
        elif Wave == 'Windowed':
            plt.plot(signal_k, signal_win_amp_cal, linewidth = 1, marker = '.', markersize = 3)
    elif Zoom == 'Part':
        assert Zoom_fin > 0
        plt.plot(signal_k[range(round(fs/Zoom_fin*Zoom_period))], signal[range(round(fs/Zoom_fin*Zoom_period))], linewidth = 1, marker = '.', markersize = 3)

    # Amplitude Spectrum Plot
    plt.figure('Amplitude Spectrum', figsize = (8, 5))
    plt.title('Amplitude Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel(Nomalized)
    plt.grid(True, which = 'both')
    #plt.xscale('log')
    plt.xscale('symlog', linthresh = 10000)
    plt.plot(fft_freq, fft_mod_amp_cal, linewidth = 1, marker = '.', markersize = 3)
    #plt.plot(fft_freq, fft_mod_amp_cal, linewidth = 1, alpha = 0.9, zorder = 100)
    if Nomalized == 'dBFS':
        _, dBFS_top = plt.ylim()
        if dBFS_top < 0:
            plt.ylim(top = 1)

    # fbase hd2 hd3 ... hd10  bins & freqs & powers
    fft_mod_amp_cal_bins = [0] * 10
    fft_mod_amp_cal_freqs = [0] * 10
    fft_mod_amp_cal_powers = [0] * 10
    for i in range(10):
        fbase_index = round(fbase * (i + 1) / fs * N)
        fft_mod_amp_cal_bins[i] = fbase_index
        fft_mod_amp_cal_freqs[i] = fft_freq[fbase_index]
        fft_mod_amp_cal_powers[i] = fft_mod_amp_cal[fbase_index]
        #plt.text(fft_mod_amp_cal_freqs[i], fft_mod_amp_cal_powers[i], '%.3f Hz, %.3f dBFS' %( fft_mod_amp_cal_freqs[i], fft_mod_amp_cal_powers[i]))

    # Marker
    colors = np.random.rand(10)
    plt.scatter(fft_mod_amp_cal_freqs, fft_mod_amp_cal_powers, s = 100, c = colors, alpha = 1, marker = 'x', zorder = 101)
    plt.text(fft_mod_amp_cal_freqs[0], fft_mod_amp_cal_powers[0], '%.3f Hz, %.3f %s' %( fft_mod_amp_cal_freqs[0], fft_mod_amp_cal_powers[0], Nomalized), zorder = 102)

    # Phase Spectrum Plot
    plt.figure('Phase Spectrum', figsize = (8, 5))
    plt.title('Phase Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Phase')
    plt.grid(True, which = 'both')
    #plt.xscale('log')
    #plt.xscale('symlog', linthreshx = 0.01)
    #plt.plot(fft_freq, fft_phase_amp_cal / math.pi, linewidth = 1, marker = '.', markersize = 3)
    plt.plot(fft_freq, fft_phase_amp_cal / math.pi, linewidth = 1)
    ymajorLocator = MultipleLocator(0.05 * math.pi)
    ymajorFormatter = FormatStrFormatter('%5.2f π')
    plt.gca().yaxis.set_major_locator(ymajorLocator)
    plt.gca().yaxis.set_major_formatter(ymajorFormatter)

    # Print Power
    print('| ------ | ------------- | --------------- |')
    for i in range(10):
        print('| %s | %10.3f Hz | %10.3f %s |'%(' BASE ' if i == 0 else 'HD%4d'%(i + 1),fft_mod_amp_cal_freqs[i], fft_mod_amp_cal_powers[i], Nomalized ))
    print('| ------ | ------------- | --------------- |')

    plt.show()

if __name__ == '__main__':
    
    # Sample Info
    N = 262144
    fs = 193986.56
    FS = 2.5
    FS_Vrms = FS / 2 / math.sqrt(2)
    Wave = 'sine'
    Wave_offset = 0
    #Wave_freq = 1001.22
    Wave_freq = 1000.105
    #Wave_freq = 1000.11

    adcout = adcmodel.adcmodel(N = N, fs = fs, FS = FS, 
        Wave = Wave, Wave_freq = Wave_freq, Wave_offset = Wave_offset,
        adc_bits = 16)
    
    # Time
    #fftplot(signal = adcout, fs = fs, Zoom = 'Part', Zoom_fin = min(Wave_freq) * 0.995, Nomalized = 'dBFS', FS = FS)
    #fftplot(signal = adcout, fs = fs, Wave = 'Windowed', Nomalized = 'dBFS', FS = FS)

    # Spectrum
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS)
    #fftplot(signal = adcout, fs = fs, Nomalized = 'Vrms')

    # Window
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS, Window = 'rectangle')
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS, Window = 'blackmanharris')
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS, Window = 'flattop')
    #fftplot(signal = adcout, fs = fs, fbase = Wave_freq, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D')
    fftplot(signal = adcout, fs = fs, fbase = Wave_freq, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D', Zoom = 'Part', Zoom_fin = Wave_freq)