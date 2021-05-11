import numpy as np
import matplotlib.pyplot as plt
import time

# CZT package
import czt

ZOOM = 10
ZOOM_RANGE = (800, 1300)

FS = 10000
N = 50
Freq = [1070, 2505, 3503]


# Time data
# T=1.0 2.0 3.0
t1 = np.arange(0, N / FS, 1 / FS)
sig1 = np.array((1.0 * np.sin(2 * np.pi * Freq[0] * t1) +
                 0.3 * np.sin(2 * np.pi * Freq[1] * t1) +
                 0.1 * np.sin(2 * np.pi * Freq[2] * t1)) * np.exp(-1e3 * t1))

# ZOOMMED
# T=1.0 1.2 1.4 1.6 1.8 2.0 2.2 2.4 2.6 2.8 3.0
t2 = np.arange(0, N / FS, 1 / FS / ZOOM)
sig2 = np.append(sig1, np.zeros((ZOOM - 1) * len(sig1)))

# All Range DFT
freq, sig_f = czt.time2freq(t1, sig1)

freq_zoom = np.arange(ZOOM_RANGE[0] * ZOOM, ZOOM_RANGE[1] * ZOOM, FS / N)
time_start = time.time()
_, sig_f_zoom = czt.time2freq(t2, sig2, freq_zoom)
time_end = time.time()
print('points', len(freq_zoom), ', totally cost', time_end - time_start)

freq_zoom /= ZOOM

print('Gen Data Calc:', Freq[0])
print('Raw Data Calc:', freq[np.argmax(np.abs(sig_f))])
print('Zoom Data Calc:', freq_zoom[np.argmax(np.abs(sig_f_zoom))])

plt.figure()
plt.plot(freq / 1e3, np.abs(sig_f), 'k', label='CZT')
plt.plot(freq_zoom / 1e3, np.abs(sig_f_zoom), 'r', label='Zoom CZT')
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")
plt.xlim([0, freq.max() / 1e3])
plt.legend()
plt.title("Frequency-domain signal")
plt.savefig("zoom-czt.png", dpi=600)


if __name__ == '__main__':
    print('czt_test')
