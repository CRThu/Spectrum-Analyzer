import czt
import numpy as np

# Reference
# https://ww2.mathworks.cn/help/signal/ref/czt.html
# https://github.com/garrettj403/CZT/

# Chirp Z-transform with zoom
# sig: ndarray, signal input
# freq_range: tuple, ex.(900, 1100), zoom freq range
# fs: double, ex.192000, sample rate
# zoom: int, zoom ratio
def czt_zoom(sig, freq_range, fs, zoom=10):

    N = len(sig)

    # Normalized
    freq_start = freq_range[0] / fs
    freq_end = freq_range[1] / fs
    freq_resolution = 1 / N / zoom

    # arange(0,5,1): 0,1,2,3,4 without 5
    # arange(0,5+1,1): 0,1,2,3,4,5 with 5
    # when double: np.arange(100.1111,105.1111+0.9998,0.9998) maybe generate 106.1009
    freq_zoomed = np.arange(freq_start, freq_end + freq_resolution, freq_resolution)

    # Interpolation
    sig = sig.copy()
    sig = np.append(sig, np.zeros((zoom - 1) * len(sig)))

    #_,czt_zoomed = czt.time2freq(np.arange(0, len(freq_zoomed), 1),sig,freq_zoomed)

    # Frequency-domain transform
    # Starting point: f[0] * dt
    A = np.exp(2j * np.pi * freq_start * 1)
    # Step: df * dt
    W = np.exp(-2j * np.pi * freq_resolution * 1)
    # Phase correction: t0 = 0
    # phase = np.exp(-2j * np.pi * 0 * freq_zoomed)
    # Chirp Z-transform
    czt_zoomed = czt.czt(sig, len(freq_zoomed), W, A)
    #sig_f_zoom = czt.czt(sig, len(freq_zoomed), W, A) * phase

    freq_zoomed *= fs

    return freq_zoomed, czt_zoomed
