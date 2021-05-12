import time

import czt
import czt_zoom
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    print('czt_test')

    fs = 10000
    gen_freq = [0.107, 0.2505, 0.3503]
    N = 50

    ZOOM = 10
    ZOOM_RANGE = 4
    ZOOM_FREQ_RANGE = ((gen_freq[0] - ZOOM_RANGE / N)
                       * fs, (gen_freq[0] + ZOOM_RANGE / N) * fs)

    # Time data
    # T=1.0 2.0 3.0
    t1 = np.arange(0, N, 1)
    sig = np.array((1.0 * np.sin(2 * np.pi * gen_freq[0] * t1) +
                    0.3 * np.sin(2 * np.pi * gen_freq[1] * t1) +
                    0.1 * np.sin(2 * np.pi * gen_freq[2] * t1)))

    # All Range DFT
    freq, sig_f = czt.time2freq(t1, sig)

    time_start = time.time()
    freq_zoomed, czt_zoomed = czt_zoom.czt_zoom(sig, ZOOM_FREQ_RANGE, fs, ZOOM)
    time_end = time.time()
    print('points', len(freq_zoomed), ', totally cost', time_end - time_start)

    print('Gen Data Calc:', gen_freq[0]*fs)
    print('Raw Data Calc:', freq[np.argmax(np.abs(sig_f))]*fs)
    print('Zoom Data Calc:', freq_zoomed[np.argmax(np.abs(czt_zoomed))])

    fft_mod = np.abs(np.fft.fftshift(np.fft.fft(sig)))
    fft_mod = fft_mod / N * 2
    sig_f = sig_f / N * 2
    czt_zoomed = czt_zoomed / N * 2

    plt.figure()
    plt.plot(freq * fs / 1e3,
             fft_mod, 'b', label='FFT')
    plt.plot(freq * fs / 1e3, np.abs(sig_f), 'k', label='CZT')
    plt.plot(freq_zoomed / 1e3, np.abs(czt_zoomed), 'r', label='Zoom CZT')
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude")
    #plt.xlim([0, freq.max() / 1e3])
    plt.legend()
    plt.title("Frequency-domain signal")
    plt.savefig("czt-zoom.png", dpi=600)

    czt_fft_err = np.abs(np.abs(fft_mod) - np.abs(sig_f))
    print('err:(', np.min(czt_fft_err), ',', np.max(czt_fft_err), ')')
