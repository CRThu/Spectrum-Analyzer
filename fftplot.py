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
    Window = 'HFT248D',
    PlotT = True, PlotSA = True, PlotSP = True,
    HDx_max = 9):
    
    #TODO Fix Bugs in Vrms
    assert Nomalized == 'dBFS'
    assert Nomalized != 'Vrms'
    #TODO Recalc Window CPG
    assert Window != 'Raw'
    assert Window != 'rectangle'
    assert Window != 'blackmanharris'
    assert Window != 'flattop'

    N = len(signal)
    half_N = int(N / 2) + 1

    # | variable        | definition                    | array length      |
    # | signal          | signal in, Time domain        | N                 |
    # | signal_k        | sample counts, Time domain    | N                 |
    # | winN            | window for fft                | N                 |
    # | signal_win      | signal in, Windowed           | N                 |
    # | signal_fft      | signal in, Spectrum domain    | int(N / 2) + 1    |
    # | fft_freq        | frequency, Spectrum domain    | int(N / 2) + 1    |
    # | fft_mod         | Amplitude, Spectrum domain    | int(N / 2) + 1    |
    # | fft_mod_dbfs    | dBFS, Spectrum domain         | int(N / 2) + 1    |
    # | fft_phase       | Phase, Spectrum domain        | int(N / 2) + 1    |
    # | fft_hd_bins     | Harmonic Bins                 | X, base + HD2-X   |
    # | fft_hd_freqs    | Harmonic distortion frequency | X, base + HD2-X   |
    # | fft_hd_amps     | Harmonic distortion amplitude | X, base + HD2-X   |
    # | fft_hd_dbfs     | Harmonic distortion dBFS      | X, base + HD2-X   |

    ### FFT ###
    signal_k = np.arange(N)

    # Window
    if fftwin.has_window(Window):
        winN = fftwin.get_window(Window, N)
    
    signal_win = winN * signal
    # FFT
    signal_fft = fft(signal_win)
    signal_fft = signal_fft[range(half_N)]

    #fft_k = np.arange(half_N)
    fft_freq = np.linspace(0, fs / 2, half_N)

    fft_mod = np.abs(signal_fft)
    fft_phase = np.angle(signal_fft)

    # FFT Nomalized : DC & Vamp
    fft_mod[0] = fft_mod[0] / N
    fft_mod[range(1,half_N)] = fft_mod[range(1,half_N)] * 2 / N

    # dBFS Calc
    fft_mod_dbfs = np.zeros(half_N)
    if Nomalized == 'dBFS':
        assert FS > 0
        # Nomalized : FS
        fft_mod_dbfs[0] = fft_mod[0] / FS
        fft_mod_dbfs[range(1,half_N)] = fft_mod[range(1,half_N)] * 2 / FS
        # Nomalized : dB
        fft_mod_dbfs = util.vratio2db_np(fft_mod_dbfs)

    # fbase hd2 hd3 ... hdx  bins & freqs & powers
    # TODO fold freq
    fft_hd_bins = np.zeros(HDx_max)
    fft_hd_freqs = np.zeros(HDx_max)
    fft_hd_amps = np.zeros(HDx_max)
    fft_hd_dbfs = np.zeros(HDx_max)
    for i in range(HDx_max):
        fbase_index = round(fbase * (i + 1) / fs * N)
        fft_hd_bins[i] = fbase_index
        fft_hd_freqs[i] = fft_freq[fbase_index]
        fft_hd_amps[i] = fft_mod[fbase_index]
        fft_hd_dbfs[i] = fft_mod_dbfs[fbase_index]

    # GUI Config
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'

    if PlotT == True:
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
                plt.plot(signal_k, signal_win, linewidth = 1, marker = '.', markersize = 3)
        elif Zoom == 'Part':
            assert Zoom_fin > 0
            plt.plot(signal_k[range(round(fs/Zoom_fin*Zoom_period))], signal[range(round(fs/Zoom_fin*Zoom_period))], linewidth = 1, marker = '.', markersize = 3)

    if PlotSA == True:
        # Amplitude Spectrum Plot
        plt.figure('Amplitude Spectrum', figsize = (8, 5))
        plt.title('Amplitude Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel(Nomalized)
        plt.grid(True, which = 'both')
        #plt.xscale('log')
        plt.xscale('symlog', linthresh = 10000)
        plt.plot(fft_freq, fft_mod_dbfs, linewidth = 1, marker = '.', markersize = 3)
        #plt.plot(fft_freq, fft_mod_dbfs, linewidth = 1, alpha = 0.9, zorder = 100)
        if Nomalized == 'dBFS':
            _, dBFS_top = plt.ylim()
            if dBFS_top < 0:
                plt.ylim(top = 1)
        
        # Marker
        colors = np.random.rand(HDx_max)
        plt.scatter(fft_hd_freqs, fft_hd_dbfs, s = 100, c = colors, alpha = 1, marker = 'x', zorder = 101)
        plt.text(fft_hd_freqs[0], fft_hd_dbfs[0], '%.3f Hz, %.3f %s' %( fft_hd_freqs[0], fft_hd_dbfs[0], Nomalized), zorder = 102)

    if PlotSP == True:
        # Phase Spectrum Plot
        plt.figure('Phase Spectrum', figsize = (8, 5))
        plt.title('Phase Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel('Phase')
        plt.grid(True, which = 'both')
        #plt.xscale('log')
        #plt.xscale('symlog', linthreshx = 0.01)
        #plt.plot(fft_freq, fft_phase / math.pi, linewidth = 1, marker = '.', markersize = 3)
        plt.plot(fft_freq, fft_phase / math.pi, linewidth = 1)
        ymajorLocator = MultipleLocator(0.05 * math.pi)
        ymajorFormatter = FormatStrFormatter('%5.2f π')
        plt.gca().yaxis.set_major_locator(ymajorLocator)
        plt.gca().yaxis.set_major_formatter(ymajorFormatter)

    # Report
    print('| ------ | ------------- | --------------- |')
    for i in range(HDx_max):
        print('| %s | %10.3f Hz | %10.3f %s |'%(' BASE ' if i == 0 else 'HD%4d'%(i + 1),fft_hd_freqs[i], fft_hd_dbfs[i], Nomalized ))
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
    #fftplot(signal = adcout, fs = fs, fbase = Wave_freq, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D', Zoom = 'Part', Zoom_fin = Wave_freq, PlotT = False, PlotSA = True, PlotSP = False)