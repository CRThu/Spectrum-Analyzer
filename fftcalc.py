import timeit

import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft

import adcmodel
import fftwin


def fftcalc(signal: np.ndarray, samplerate: float = None, window: str = None, normalized=True):
    if signal.ndim == 1:
        up_dim = True
        signal = signal.reshape(1, -1)

    N = len(signal[0])
    half_N = int(N / 2) + 1

    if samplerate is None:
        samplerate = N
    if window is None:
        window = 'rectangle'

    # Window
    # winN = signal.blackmanharris(N)
    if fftwin.has_window(window):
        winN = fftwin.get_window(window, N)

    signal_win = winN * signal

    signal_fft = fft(signal_win)
    signal_fft = signal_fft[:, :half_N]

    fft_freq = np.linspace(0, samplerate / 2, half_N)

    fft_mod = np.abs(signal_fft)
    fft_phase = np.angle(signal_fft)

    # FFT Nomalized : DC & Vamp
    if normalized:
        fft_mod[:, 0] = fft_mod[:, 0] / N
        fft_mod[:, 1:] = fft_mod[:, 1:] * (2 / N)

    if up_dim:
        return fft_freq, fft_mod[0], fft_phase[0]
    else:
        return fft_freq, fft_mod, fft_phase


if __name__ == '__main__':
    adcout = adcmodel.adcmodel()
    f, m, p = fftcalc(adcout)
    print(adcout.shape, f.shape, m.shape, p.shape)

    print('timeit 1000 times for %d points FFT (sec):' % len(adcout),
          timeit.timeit(stmt=lambda: fftcalc(adcout), number=1000))

    fig = plt.figure()
    ax1 = fig.gca()
    ax1.grid(True, which='both')
    ax1.plot(f, m, 'blue')
    ax2 = ax1.twinx()
    ax2.plot(f, p, 'orange')
    plt.show()
