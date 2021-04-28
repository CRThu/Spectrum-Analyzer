import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import mpl
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from scipy import signal as wd
from scipy.fftpack import fft, ifft

import adcmodel
import analysis_util as util
import fftwin

info = {
    'name': 'FFT ANALYSIS PROGRAM',
    'project': '202116A',
    'version': '0.0.1',
    'release': 'alpha',
    'author': 'written by carrot',
}


def fftplot(signal, fs, fbase,
            Wave='Raw',
            Zoom='All', Zoom_fin=-1, Zoom_period=3,
            Nomalized='dBFS', FS=-1,
            Window='HFT248D',
            PlotT=True, PlotSA=True, PlotSP=True,
            HDx_max=9,
            dBm_Z=600):

    # TODO Fix Bugs in Vrms
    assert Nomalized == 'dBFS'
    assert Nomalized != 'dBm'
    assert Nomalized != 'Vrms'
    # TODO Recalc Window CPG
    assert Window != 'Raw'
    assert Window != 'rectangle'
    #assert Window != 'blackmanharris'
    assert Window != 'flattop'
    # TODO calc fbase when not given

    N = len(signal)
    half_N = int(N / 2) + 1

    # | variable                | definition                    | length            |
    # | signal                  | signal in, Time domain        | N                 |
    # | signal_k                | sample counts, Time domain    | N                 |
    # | winN                    | window for fft                | N                 |
    # | signal_win              | signal in, Windowed           | N                 |
    # | signal_fft              | signal in, Spectrum domain    | int(N / 2) + 1    |
    # | fft_freq                | frequency, Spectrum domain    | int(N / 2) + 1    |
    # | fft_mod                 | Amplitude, Spectrum domain    | int(N / 2) + 1    |
    # | fft_mod_dbfs            | dBFS, Spectrum domain         | int(N / 2) + 1    |
    # | fft_phase               | Phase, Spectrum domain        | int(N / 2) + 1    |
    # | fft_hd_bins             | Harmonic Bins                 | X, base + HD2-X   |
    # | fft_hd_freqs            | Harmonic frequency            | X, base + HD2-X   |
    # | fft_hd_amps             | Harmonic distortion amplitude | X, base + HD2-X   |
    # | fft_hd_dbfs             | Harmonic distortion dBFS      | X, base + HD2-X   |
    # | fft_mod_spur            | Spurious Amplitude            | int(N / 2) + 1    |
    # | fft_spur_bin            | Peak spurious Bins            | 1                 |
    # | fft_spur_freq           | Peak spurious frequency       | 1                 |
    # | fft_spur_amp            | Peak spurious Noise amplitude | 1                 |
    # | fft_spur_dbfs           | Peak spurious Noise dBFS      | 1                 |
    # | fft_mod_noise           | Noise Spectrum                | int(N / 2) + 1    |
    # | fft_mod_noise_inband    | Noise Spectrum in band        | BW / fres         |
    # | fft_noise_inband_amp    | Noise Amplitude in band       | 1                 |
    # | fft_noise_inband_vrms   | Noise Vrms in band            | 1                 |
    # | fft_noise_inband_power  | Noise Power in band           | 1                 |
    # | fft_signal_vrms         | Signal Vrms in band           | 1                 |
    # | fft_signal_power        | Signal Power in band          | 1                 |

    ### FFT ###
    signal_k = np.arange(N)

    # Window
    #winN = wd.blackmanharris(N)
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
    fft_mod[range(1, half_N)] = fft_mod[range(1, half_N)] * 2 / N

    # dBFS Calc
    fft_mod_dbfs = np.zeros(half_N)
    assert FS > 0
    # Nomalized : FS
    fft_mod_dbfs[0] = fft_mod[0] / FS
    fft_mod_dbfs[range(1, half_N)] = fft_mod[range(1, half_N)] * 2 / FS
    # Nomalized : dB
    fft_mod_dbfs = util.vratio2db_np(fft_mod_dbfs)

    ### ANALYSIS ###
    # Harmonic distortion
    # fbase hd2 hd3 ... hdx  bins & freqs & powers
    # TODO del fbase in hdx
    # TODO fold freq
    fft_hd_bins = np.zeros(HDx_max, dtype=int)
    fft_hd_freqs = np.zeros(HDx_max)
    fft_hd_amps = np.zeros(HDx_max)
    fft_hd_dbfs = np.zeros(HDx_max)
    for i in range(HDx_max):
        fbase_index = round(fbase * (i + 1) / fs * N)
        fft_hd_bins[i] = fbase_index
        fft_hd_freqs[i] = fft_freq[fbase_index]
        fft_hd_amps[i] = fft_mod[fbase_index]
        fft_hd_dbfs[i] = fft_mod_dbfs[fbase_index]

    # Spurious
    # Peak Harmonic or Spurious Noise
    # Calc peak power except [DC : DC + L], [Signal - L : Signal + L]
    signal_bin = fft_hd_bins[0]
    current_window_mainlobe = fftwin.get_window_mainlobe_width(window=Window)
    fft_mod_spur = np.copy(fft_mod)
    fft_mod_spur[0: 0 + current_window_mainlobe + 1] = 0
    fft_mod_spur[signal_bin - current_window_mainlobe:signal_bin +
                 current_window_mainlobe + 1] = 0
    fft_spur_bin = np.argmax(fft_mod_spur)
    fft_spur_freq = fft_freq[fft_spur_bin]
    fft_spur_amp = fft_mod[fft_spur_bin]
    fft_spur_dbfs = fft_mod_dbfs[fft_spur_bin]

    # Noise
    # Calc peak power except [DC : DC + L], [Signal - L : Signal + L], [HDx - L : HDx + L]
    # Voltage to Power
    # TODO add noise in masked bin
    fft_mod_noise = np.copy(fft_mod)
    fft_mod_noise[0: 0 + current_window_mainlobe + 1] = 0
    for i in range(HDx_max):
        fft_mod_noise[fft_hd_bins[i] - current_window_mainlobe:
                      fft_hd_bins[i] + current_window_mainlobe + 1] = 0
    fft_mod_noise_inband = fft_mod_noise[:]
    fft_noise_inband_amp = np.linalg.norm(fft_mod_noise_inband)
    # Pn_true = Pn - ENBW
    fft_noise_inband_amp /= fftwin.get_window_ENBW(Window) ** 0.5

    # Power
    # Signal
    fft_signal_vrms = util.vamp2vrms(fft_hd_amps[0])
    fft_signal_power = util.vamp2dbm(fft_hd_amps[0], Z=dBm_Z)

    # Harmonic
    fft_harmonic_amps = np.linalg.norm(fft_hd_amps[1:])
    fft_harmonic_vrms = util.vamp2vrms(fft_harmonic_amps)
    fft_harmonic_power = util.vamp2dbm(fft_harmonic_amps, Z=dBm_Z)

    # Noise
    fft_noise_inband_vrms = util.vamp2vrms(fft_noise_inband_amp)
    fft_noise_inband_power = util.vamp2dbm(fft_noise_inband_amp, Z=dBm_Z)

    # Performance
    perf_dic = util.perf_calc(
        FS=FS,
        vs=fft_hd_amps[0],
        vd=fft_harmonic_amps,
        vn=fft_noise_inband_amp,
        vspur=fft_spur_amp)

    ### GUI ###
    # GUI Config
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'

    if PlotT == True:
        # Time Domain Plot
        plt.figure('Time', figsize=(8, 5))
        plt.title('Time')
        plt.xlabel('Samples')
        plt.ylabel('Voltage')
        plt.grid(True, which='both')
        if Zoom == 'All':
            if Wave == 'Raw':
                #plt.plot(signal_k, signal, linewidth = 1, marker = '.', markersize = 3)
                plt.plot(signal_k, signal, linewidth=1)
            elif Wave == 'Windowed':
                plt.plot(signal_k, signal_win,
                         linewidth=1, marker='.', markersize=3)
        elif Zoom == 'Part':
            assert Zoom_fin > 0
            plt.plot(signal_k[range(round(fs / Zoom_fin * Zoom_period))],
                     signal[range(round(fs / Zoom_fin * Zoom_period))],
                     linewidth=1, marker='.', markersize=3)

    if PlotSA == True:
        # Amplitude Spectrum Plot
        plt.figure('Amplitude Spectrum', figsize=(8, 5))
        plt.title('Amplitude Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel(Nomalized)
        plt.grid(True, which='both')
        # plt.xscale('log')
        plt.xscale('symlog', linthresh=10000)
        #plt.plot(fft_freq, fft_mod_dbfs, linewidth = 1, marker = '.', markersize = 3)
        plt.plot(fft_freq, fft_mod_dbfs, linewidth=1, alpha=0.9, zorder=100)
        if Nomalized == 'dBFS':
            _, dBFS_top = plt.ylim()
            if dBFS_top < 0:
                plt.ylim(top=1)

        # Marker
        # HDx
        colors = np.random.rand(HDx_max)
        plt.scatter(fft_hd_freqs, fft_hd_dbfs,
                    s=100, c=colors, alpha=1, marker='x', zorder=101)
        plt.text(fft_hd_freqs[0], fft_hd_dbfs[0], '%.3f Hz, %.3f %s'
                 % (fft_hd_freqs[0], fft_hd_dbfs[0], Nomalized), zorder=102)
        # Spur
        colors = np.random.rand(1)
        plt.scatter(fft_spur_freq, fft_spur_dbfs,
                    s=100, c=colors, alpha=1, marker='+', zorder=103)

    if PlotSP == True:
        # Phase Spectrum Plot
        plt.figure('Phase Spectrum', figsize=(8, 5))
        plt.title('Phase Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel('Phase')
        plt.grid(True, which='both')
        # plt.xscale('log')
        #plt.xscale('symlog', linthreshx = 0.01)
        #plt.plot(fft_freq, fft_phase / math.pi, linewidth = 1, marker = '.', markersize = 3)
        plt.plot(fft_freq, fft_phase / math.pi, linewidth=1)
        ymajorLocator = MultipleLocator(0.05 * math.pi)
        ymajorFormatter = FormatStrFormatter('%5.2f π')
        plt.gca().yaxis.set_major_locator(ymajorLocator)
        plt.gca().yaxis.set_major_formatter(ymajorFormatter)

    ### REPORT ###
    # Report
    print('| ------ | --------------- | --------------- |')
    # HDx
    for i in range(HDx_max):
        print('| %-6s | %12.3f Hz | %10.3f %s |'
              % ('BASE' if i == 0 else 'HD%2d' % (i + 1),
                  fft_hd_freqs[i], fft_hd_dbfs[i], Nomalized))
    print('| ------ | --------------- | --------------- |')

    # Spurious
    print('| %-6s | %12.3f Hz | %10.3f %s |'
          % ('SPUR', fft_spur_freq, fft_spur_dbfs, Nomalized))
    print('| ------ | --------------- | --------------- |')

    # Power
    print('| %-6s | %9.3f %s | %11.3f dBm |'
          % (('Ps',)
             + util.range_format(fft_signal_vrms, 'Vrms')
             + (fft_signal_power,)))
    print('| %-6s | %9.3f %s | %11.3f dBm |'
          % (('Ph',)
             + util.range_format(fft_harmonic_vrms, 'Vrms')
             + (fft_harmonic_power,)))
    print('| %-6s | %9.3f %s | %11.3f dBm |'
          % (('Pn',)
             + util.range_format(fft_noise_inband_vrms, 'Vrms')
             + (fft_noise_inband_power,)))
    print('| ------ | --------------- | --------------- |')

    # Perforance
    for key, value in perf_dic.items():
        print('| %-6s | %9.3f %5s |' % ((key,) + value))
    print('| ------ | --------------- |')

    if PlotT or PlotSA or PlotSP:
        plt.show()


if __name__ == '__main__':

    # Sample Info
    N = 262144
    fs = 193986.56
    FS = 2.5
    FS_Vrms = FS / 2 / math.sqrt(2)
    Wave = 'sine'
    Wave_offset = 0
    Wave_freq = 1001.22
    #Wave_freq = 1000.105
    #Wave_freq = 1000.11

    adcout = adcmodel.adcmodel(N=N, fs=fs, FS=FS,
                               Wave=Wave, Wave_freq=Wave_freq, Wave_offset=Wave_offset, Wave_Vrms=0.7746, HDx=[-95, -90, -100],
                               adc_bits=None, DR=100)

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
    #fftplot(signal = adcout, fs = fs, fbase = Wave_freq, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D', Zoom = 'Part', Zoom_fin = Wave_freq)
    fftplot(signal=adcout, fs=fs, fbase=Wave_freq, Nomalized='dBFS', FS=FS, Window='HFT248D',
            Zoom='Part', Zoom_fin=Wave_freq, PlotT=False, PlotSA=True, PlotSP=False)
