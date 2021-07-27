import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import mpl
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from scipy import signal as wd
from scipy.fftpack import fft, ifft

import adcmodel
import analysis_util as util
import czt_zoom
import fftwin

info = {
    'name': 'SPECTRUM ANALYZER PROGRAM',
    'project': '202116A',
    'version': '2.0',
    'release': 'beta',
    'author': 'programed by carrot',
}


def fftplot(signal, fs,
            noise_band=None, spurious_existed_freqs=((),),
            Wave='Raw',
            Zoom='All', Zoom_fin=None, Zoom_period=3,
            Nomalized='dBFS', FS=None,
            Window='HFT248D',
            czt_zoom_window='blackmanharris', czt_zoom_ratio=10,
            Noise_corr=True,
            PlotT=True, PlotSA=True, PlotSP=True,
            HDx_max=9,
            dBm_Z=600,
            mpl_plot=True
            ):

    # TODO add dBm
    assert Nomalized == 'dBFS'
    assert Nomalized != 'dBm'
    # TODO Recalc Window CPG
    assert Window != 'flattop'

    FS_Vamp = util.vpp2vamp(FS)

    N = len(signal)
    half_N = int(N / 2) + 1

    # | variable                | definition                    | length            |
    # | signal                  | signal in, Time domain        | N                 |
    # | signal_k                | sample counts, Time domain    | N                 |
    # | winN                    | window for fft                | N                 |
    # | signal_win              | signal in, Windowed           | N                 |
    # | signal_fft              | signal in, Spectrum domain    | int(N / 2) + 1    |
    # | fft_freq                | frequency, Spectrum domain    | int(N / 2) + 1    |
    # | fft_mod                 | Magnitude, Spectrum domain    | int(N / 2) + 1    |
    # | fft_phase               | Phase, Spectrum domain        | int(N / 2) + 1    |
    # | fft_mod_dbfs            | dBFS, Spectrum domain         | int(N / 2) + 1    |
    # | fft_mod_len             | length of fft_mod             | 1                 |
    # | current_window_mainlobe | current window mainlobe       | 1                 |
    # | mask_bins_dc            | mask bins tuple, dc           | tuple             |
    # | mask_bins_signal        | mask bins tuple, signal       | tuple             |
    # | mask_bins_hd            | mask bins tuple, distortion   | tuple             |
    # | guess_signal_bin        | signal bin position           | 1                 |
    # | guess_hd_bins           | distortion bins positions     | X - 1, HD2-X      |
    # | fft_signal_bin          | Peak signal Bins              | 1                 |
    # | fft_signal_freq         | Peak signal frequency         | 1                 |
    # | fft_signal_amp          | Peak signal Noise amplitude   | 1                 |
    # | fft_signal_dbfs         | Peak signal Noise dBFS        | 1                 |
    # | fft_hd_bins             | Harmonic Bins                 | X - 1, HD2-X      |
    # | fft_hd_freqs            | Harmonic frequency            | X - 1, HD2-X      |
    # | fft_hd_amps             | Harmonic distortion amplitude | X - 1, HD2-X      |
    # | fft_hd_dbfs             | Harmonic distortion dBFS      | X - 1, HD2-X      |
    # | fft_mod_spur            | Spurious Amplitude            | int(N / 2) + 1    |
    # | fft_spur_bin            | Peak spurious Bins            | 1                 |
    # | fft_spur_freq           | Peak spurious frequency       | 1                 |
    # | fft_spur_amp            | Peak spurious Noise amplitude | 1                 |
    # | fft_spur_dbfs           | Peak spurious Noise dBFS      | 1                 |
    # | fft_mod_noise           | Noise Spectrum                | int(N / 2) + 1    |
    # | fft_mod_noise_mid       | Noise Median for correction   | 1                 |
    # | fft_mod_noise_inband    | Noise Spectrum in band        | BW / fres         |
    # | fft_noise_inband_amp    | Noise Amplitude in band       | 1                 |
    # | fft_signal_vrms         | Signal Vrms in band           | 1                 |
    # | fft_signal_power        | Signal Power in band          | 1                 |
    # | fft_thd_amp             | Distortion amplitude          | 1                 |
    # | fft_thd_vrms            | Distortion Vrms in band       | 1                 |
    # | fft_thd_power           | Distortion Power in band      | 1                 |
    # | fft_noise_inband_vrms   | Noise Vrms in band            | 1                 |
    # | fft_noise_inband_power  | Noise Power in band           | 1                 |
    # | perf_dict               | Performance Dictionary        | ~8                |

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
    fft_mod_dbfs = fft_mod / FS_Vamp
    # Nomalized : dB
    fft_mod_dbfs = util.vratio2db_np(fft_mod_dbfs)

    ### ANALYSIS ###
    # Generate Mask bins
    fft_mod_len = len(fft_mod)
    current_window_mainlobe = fftwin.get_window_mainlobe_width(window=Window)
    # mask_bins_dc : [DC : DC + L]
    mask_bins_dc = util.mask_bins_gen(
        [0], current_window_mainlobe, fft_mod_len)
    # Guess signal bin
    guess_signal_bin = util.guess_fft_signal_bin(fft_mod, mask_bins_dc)
    guess_signal_bin_err_range = (
        guess_signal_bin - 1, guess_signal_bin + 1)
    # Guess exact signal bin
    bins_zoomed, czt_zoomed = czt_zoom.czt_zoom(
        signal * fftwin.get_window(czt_zoom_window, N), guess_signal_bin_err_range, N, zoom=czt_zoom_ratio)
    guess_exact_signal_bin = bins_zoomed[np.argmax(abs(czt_zoomed))]
    # Guess harmonic distortion bin
    guess_exact_hd_bins = util.guess_fft_hd_bin(
        guess_exact_signal_bin, HDx_max, N)
    guess_hd_bins = np.round(guess_exact_hd_bins).astype(int)

    # mask_bins_signal : [Signal - L : Signal + L]
    mask_bins_signal = util.mask_bins_gen(
        [guess_signal_bin], current_window_mainlobe, fft_mod_len)
    # mask_bins_hd : [HDx - L : HDx + L]
    mask_bins_hd = util.mask_bins_gen(
        guess_hd_bins, current_window_mainlobe, fft_mod_len)

    # Signal
    fft_signal_bin = guess_signal_bin
    fft_signal_freq = fft_freq[guess_signal_bin]
    fft_exact_signal_freq = guess_exact_signal_bin / N * fs
    fft_signal_amp = fft_mod[guess_signal_bin]
    fft_signal_dbfs = fft_mod_dbfs[guess_signal_bin]

    # Harmonic distortion
    # hd2 hd3 ... hdx  bins & freqs & powers
    # TODO: Find peak power around distortion
    fft_hd_bins = guess_hd_bins
    fft_hd_freqs = [fft_freq[x] for x in fft_hd_bins]
    fft_exact_hd_freqs = guess_exact_hd_bins / N * fs
    fft_hd_amps = [fft_mod[x] for x in fft_hd_bins]
    fft_hd_dbfs = [fft_mod_dbfs[x] for x in fft_hd_bins]

    # Spurious
    # throw exist spurious
    spurious_existed_bins = ((),)
    for spurious_existed_freq in spurious_existed_freqs:
        if len(spurious_existed_freq) == 2:
            spurious_existed_bins += ((int(spurious_existed_freq[0] / (fs / N)),
                                       int(spurious_existed_freq[1] / (fs / N))),)
    # Peak Harmonic distortion or Spurious Noise
    # Calc peak power except [DC : DC + L], [Signal - L : Signal + L]
    fft_mod_spur = util.mask_array(
        fft_mod, mask_bins_dc + mask_bins_signal + spurious_existed_bins)
    fft_spur_bin = np.argmax(fft_mod_spur)
    fft_spur_freq = fft_freq[fft_spur_bin]
    fft_spur_amp = fft_mod[fft_spur_bin]
    fft_spur_dbfs = fft_mod_dbfs[fft_spur_bin]

    # Noise
    # Calc peak power except [DC : DC + L], [Signal - L : Signal + L], [HDx - L : HDx + L]
    fft_mod_noise = util.mask_array(
        fft_mod, mask_bins_dc + mask_bins_signal + mask_bins_hd + spurious_existed_bins)
    # Noise Correction for mask
    if Noise_corr == True:
        fft_mod_noise_mid = np.median(fft_mod_noise)
        fft_mod_noise = util.mask_array(
            fft_mod, mask_bins_dc + mask_bins_signal + mask_bins_hd + spurious_existed_bins, fill=fft_mod_noise_mid)

    # noise_band
    fft_mod_noise_inband = fft_mod_noise[:]
    if noise_band is not None:
        fft_mod_noise_inband = fft_mod_noise[:int(noise_band / fs * N) + 1]
    fft_noise_inband_amp = np.linalg.norm(fft_mod_noise_inband)
    # Pn_true = Pn - ENBW
    fft_noise_inband_amp /= fftwin.get_window_ENBW(Window) ** 0.5

    # Power
    # Signal
    fft_signal_vrms = util.vamp2vrms(fft_signal_amp)
    fft_signal_power = util.vamp2dbm(fft_signal_amp, Z=dBm_Z)

    # Total Harmonic Distortion
    fft_thd_amp = np.linalg.norm(fft_hd_amps)
    fft_thd_vrms = util.vamp2vrms(fft_thd_amp)
    fft_thd_power = util.vamp2dbm(fft_thd_amp, Z=dBm_Z)

    # Noise
    fft_noise_inband_vrms = util.vamp2vrms(fft_noise_inband_amp)
    fft_noise_inband_power = util.vamp2dbm(fft_noise_inband_amp, Z=dBm_Z)

    # Performance
    perf_dict = util.perf_calc(
        FS=FS,
        vs=fft_signal_amp,
        vd=fft_thd_amp,
        vn=fft_noise_inband_amp,
        vspur=fft_spur_amp)

    ### GUI ###
    mpl_figs = []
    # GUI Config
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['mathtext.fontset'] = 'cm'

    if PlotT == True:
        # Time Domain Plot
        fig = plt.figure(figsize=(8, 5))
        ax = fig.gca()
        ax.set_title('Time', fontsize=16)
        ax.set_xlabel('Samples')
        ax.set_ylabel('Voltage')
        ax.grid(True, which='both')
        if Zoom == 'All':
            if Wave == 'Raw':
                #ax.plot(signal_k, signal, linewidth = 1, marker = '.', markersize = 2)
                ax.plot(signal_k, signal, linewidth=1)
            elif Wave == 'Windowed':
                ax.plot(signal_k, signal_win,
                        linewidth=1, marker='.', markersize=2)
        elif Zoom == 'Part':
            assert Zoom_fin > 0
            ax.plot(signal_k[range(round(fs / Zoom_fin * Zoom_period))],
                    signal[range(round(fs / Zoom_fin * Zoom_period))],
                    linewidth=1, marker='.', markersize=2)
        mpl_figs.append(fig)

    if PlotSA == True:
        # Magnitude Spectrum Plot
        fig = plt.figure(figsize=(8, 5))
        ax = fig.gca()
        ax.set_title('Magnitude Spectrum', fontsize=16)
        ax.set_xlabel('Frequency')
        ax.set_ylabel(Nomalized)
        ax.grid(True, which='both')
        # ax.set_xscale('log')
        ax.set_xscale('symlog', linthresh=fs / 10)
        #ax.plot(fft_freq, fft_mod_dbfs, linewidth = 1, marker = '.', markersize = 3)
        ax.plot(fft_freq, fft_mod_dbfs, linewidth=1, alpha=0.9, zorder=100)
        if Nomalized == 'dBFS':
            _, dBFS_top = ax.set_ylim()
            if dBFS_top < 0:
                ax.set_ylim(top=1)

        # Marker
        # Signal & HDx
        colors = np.random.rand(HDx_max)
        ax.scatter(np.append([fft_exact_signal_freq, ], fft_exact_hd_freqs), np.append([fft_signal_dbfs, ], fft_hd_dbfs),
                   s=100, c=colors, alpha=1, marker='x', zorder=101)
        ax.text(fft_exact_signal_freq, fft_signal_dbfs, '%.3f Hz, %.3f %s'
                % (fft_exact_signal_freq, fft_signal_dbfs, Nomalized), zorder=102)
        # Spur
        colors = np.random.rand(1)
        ax.scatter(fft_spur_freq, fft_spur_dbfs,
                   s=100, c=colors, alpha=1, marker='+', zorder=103)
        mpl_figs.append(fig)

    if PlotSP == True:
        # Phase Spectrum Plot
        fig = plt.figure(figsize=(8, 5))
        ax = fig.gca()
        ax.set_title('Phase Spectrum', fontsize=16)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Phase')
        ax.grid(True, which='both')
        # ax.set_xscale('log')
        #ax.set_xscale('symlog', linthreshx = 0.01)
        #ax.plot(fft_freq, fft_phase / math.pi, linewidth = 1, marker = '.', markersize = 3)
        ax.plot(fft_freq, fft_phase / math.pi, linewidth=1)
        ymajorLocator = MultipleLocator(0.05 * math.pi)
        ymajorFormatter = FormatStrFormatter('%5.2f π')
        ax.yaxis.set_major_locator(ymajorLocator)
        ax.yaxis.set_major_formatter(ymajorFormatter)
        mpl_figs.append(fig)

    ### REPORT ###
    # Report
    print('| ------ | --------------- | --------------- |')
    # Base
    print('| %-6s | %12.3f Hz | %10.3f %s |'
          % ('BASE', fft_exact_signal_freq, fft_signal_dbfs, Nomalized))
    # HDx
    for i in range(HDx_max - 1):
        print('| %-6s | %12.3f Hz | %10.3f %s |'
              % ('HD%2d' % (i + 2),
                  fft_exact_hd_freqs[i], fft_hd_dbfs[i], Nomalized))
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
             + util.range_format(fft_thd_vrms, 'Vrms')
             + (fft_thd_power,)))
    print('| %-6s | %9.3f %s | %11.3f dBm |'
          % (('Pn',)
             + util.range_format(fft_noise_inband_vrms, 'Vrms')
             + (fft_noise_inband_power,)))
    print('| ------ | --------------- | --------------- |')

    # Perforance
    for key, value in perf_dict.items():
        print('| %-6s | %9.3f %5s |' % ((key,) + value))
    print('| ------ | --------------- |')

    # TEST CZT ZOOM RANGE
    # plt.figure('Test Spectrum', figsize=(8, 5))
    # plt.title('Magnitude Spectrum')
    # plt.xlabel('Frequency')
    # plt.ylabel('V')
    # plt.grid(True, which='both')
    # plt.plot(bins_zoomed/N*fs, abs(czt_zoomed)/N*2, linewidth=1, color='red', alpha=0.9, zorder=101)
    # plt.plot(fft_freq, fft_mod, linewidth=1, color='black', alpha=0.9, zorder=100)
    # plt.xlim(bins_zoomed[0]/N*fs-3,bins_zoomed[-1]/N*fs+3)

    if mpl_plot:
        if PlotT or PlotSA or PlotSP:
            plt.show()
            
    return mpl_figs


if __name__ == '__main__':

    # Sample Info
    N = 16384
    fs = 193986.56
    FS = 2.5
    FS_Vrms = FS / 2 / math.sqrt(2)
    #Wave_Vrms = 0.776
    Wave_Vrms = FS_Vrms
    Wave = 'sine'
    Wave_offset = 0
    #Wave_freq = 1001.22
    #Wave_freq = 1000.105
    Wave_freq = 1000.11

    adcout = adcmodel.adcmodel(N=N, fs=fs, FS=FS,
                               HDx=[-95, -90, -100],
                               Wave=Wave, Wave_freq=Wave_freq, Wave_offset=Wave_offset, Wave_Vrms=Wave_Vrms,
                               adc_bits=None, DR=100)

    print('Data length = %d, Range = [%f,%f]' % (
        len(adcout), np.min(adcout), np.max(adcout)))

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
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D')
    #fftplot(signal = adcout, fs = fs, Nomalized = 'dBFS', FS = FS, Window = 'HFT248D', Zoom = 'Part', Zoom_fin = Wave_freq)
    fftplot(signal=adcout, fs=fs, Nomalized='dBFS', FS=FS, Window='HFT248D',
            Zoom='Part', Zoom_fin=Wave_freq,  # noise_band=0.5 * fs / 2,
            PlotT=True, PlotSA=True, PlotSP=False)
