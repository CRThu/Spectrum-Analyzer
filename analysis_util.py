import math

import numpy as np


def wgn(x, snr):
    snr_db = 10 ** (snr / 10.0)
    xpower = np.sum(x ** 2) / len(x)
    npower = xpower / snr_db
    return np.random.randn(len(x)) * np.sqrt(npower)


def wgn_dr(FS, DR, N):
    dr_db = db2pratio(DR)
    xpower = vpp2vrms(FS) ** 2
    npower = xpower / dr_db
    return np.random.randn(N) * np.sqrt(npower)

### dB <-> Ratio ###
# real
def db2vratio(db):
    return math.pow(10, db / 20)


def vratio2db(ratio):
    return 20 * math.log10(ratio)


def db2pratio(db):
    return math.pow(10, db / 10)


def pratio2db(ratio):
    return 10 * math.log10(ratio)

# numpy
def db2vratio_np(db):
    return np.power(10, db / 20)


def vratio2db_np(ratio):
    return 20 * np.log10(ratio)


def db2pratio_np(db):
    return np.power(10, db / 10)


def pratio2db_np(ratio):
    return 10 * np.log10(ratio)

### Vrms <-> Vpp <-> Vamp ###
def vrms2vpp(vrms):
    return (vrms * math.sqrt(2) * 2)

def vpp2vrms(vpp):
    return (vpp / math.sqrt(2) / 2)

def vrms2vamp(vrms):
    return (vrms * math.sqrt(2))

def vamp2vrms(amp):
    return (amp / math.sqrt(2))

def vamp2vpp(amp):
    return (amp * 2)

def vpp2vamp(vpp):
    return (vpp / 2)

### Vamp <-> Power <-> dBm ###
def vamp2power(amp, Z=600):
    return (amp / math.sqrt(2)) ** 2 / Z


def vrms2power(vrms, Z=600):
    return vrms ** 2 / Z

# 0 dBm = 1 mW
# 30 dBm = 1 W
def vamp2dbm(amp, Z=600):
    return 10 * math.log10((amp / math.sqrt(2)) ** 2 / Z * 1000)


def vrms2dbm(vrms, Z=600):
    return 10 * math.log10(vrms ** 2 / Z * 1000)


### f <-> p <-> n <-> u <-> m <-> 1 <-> k <-> M <-> G <-> T ###
# Voltage/Watt Range Convert
# example: 1.234 V | 123.4 mV | 123.4 uV
def range_format(x, range_str=None):
    # Const Range String
    range_prefix = 'fpnum kMGT'
    range_prefix_default_cur = range_prefix.find(' ')
    assert range_prefix_default_cur != -1

    range_cur = range_prefix_default_cur
    range_raw_has_prefix = False
    if range_str is not None:
        range_strin_cur = range_prefix.find(range_str[0])
        if range_strin_cur != -1:
            range_cur = range_strin_cur
            range_raw_has_prefix = True

    while True:
        if range_cur == 0 or range_cur == len(range_prefix) - 1:
            break
        if int(x) == 0:
            # Lower Range
            x *= 1000
            range_cur -= 1
        elif int(x) >= 1000:
            # Higher Range
            x /= 1000
            range_cur += 1
        else:
            break

    if range_raw_has_prefix:
        range_str = range_prefix[range_cur] + range_str[1:]
    else:
        range_str = range_prefix[range_cur] + \
            ('' if range_str is None else range_str)

    return x, range_str

# Calc Perforance
# input(Vamp): signal power, distortion power, noise power
# Key: DR, SNR, THD, THD+N, SINAD, SFDR, SFDRFS, ENOB
def perf_calc(FS, vs, vd, vn, vspur):
    # FS vpp to vamp
    FS = vpp2vamp(FS)
    perf_dic = {
        'DR': (vratio2db(FS / vn), 'dB'),
        'SNR': (vratio2db(vs / vn), 'dB'),
        'THD': (-vratio2db(vs / vd), 'dB'),
        'THD+N': (-vratio2db(vs / (vd + vn)), 'dB'),
        'SINAD': (vratio2db(vs / (vd + vn)), 'dB'),
        'SFDR': (-vratio2db(vs / vspur), 'dBc'),
        'SFDRFS': (-vratio2db(FS / vspur), 'dBFS'),
        'ENOB': ((vratio2db(vs / (vd + vn)) - 1.76 + vratio2db(FS / vs)) / 6.02, 'Bits'),
    }

    return perf_dic

# Generate mask for nparray
# mask_bins is tuple. such as ((0,10),(20,50))
def mask_bins_gen(center_bins, mainlobe, arr_len):
    index_max = arr_len - 1
    mask_bins = ()
    for center_bin in center_bins:
        center_bin_min = center_bin - mainlobe
        center_bin_max = center_bin + mainlobe
        if center_bin_min < 0:
            center_bin_min = 0
        elif center_bin_min > index_max:
            center_bin_min = index_max
        if center_bin_max < 0:
            center_bin_max = 0
        elif center_bin_max > index_max:
            center_bin_max = index_max
        mask_bins += ((center_bin_min, center_bin_max),)
    return mask_bins

# Add mask for nparray
# mask_bins is tuple. such as ((0,10),(20,50))
def mask_array(arr_in, mask_bins, fill=0):
    arr = np.array(arr_in).copy()
    for mask_bin in mask_bins:
        if len(mask_bin) == 2:
            if mask_bin[0] < 0 or mask_bin[0] > len(arr) - 1 \
                    or mask_bin[1] < 0 or mask_bin[1] > len(arr) - 1 \
                    or mask_bin[0] > mask_bin[1]:
                raise IndexError('mask = [%d, %d] out of range: [%d, %d]' % (
                    mask_bin[0], mask_bin[1], 0, len(arr) - 1))
            else:
                arr[mask_bin[0]:mask_bin[1] + 1] = fill
    return arr

# Guess Signal Freq
# fft_mod is nparray
# mask_bins is tuple. such as ((0,10),(20,50))
# if prob_bin is not none, find bins around prob_bin first
# Err = +/- 0.5 Bins
def guess_fft_signal_bin(fft_mod, mask_bins=(), prob_bin=None, prob_bin_mainlobe=None):
    fft_mod_mask = mask_array(fft_mod, mask_bins, fill=0)
    if prob_bin is None:
        return np.argmax(fft_mod_mask)
    else:
        prob_bin_min = prob_bin - prob_bin_mainlobe
        prob_bin_max = prob_bin + prob_bin_mainlobe
        index_max = len(fft_mod) - 1
        if prob_bin_min < 0:
            prob_bin_min = 0
        elif prob_bin_min > index_max:
            prob_bin_min = index_max
        if prob_bin_max < 0:
            prob_bin_max = 0
        elif prob_bin_max > index_max:
            prob_bin_max = index_max
        return np.argmax(fft_mod_mask[prob_bin_min:prob_bin_max + 1]) + prob_bin_min

# Guess Distortion Freq
# Generate 2 - HDx_max harmonic bins
# Err = +/- Signal_Err * HDx Bins
# Fold freq out of the 1st Nyquist zone
# abs(+/-K*fs +/-fa)
# K=0: fa
# K=1: fs-fa    fs+fa
# K=2: 2fs-fa   2fs+fa
def guess_fft_hd_bin(guess_signal_bin, HDx_max, N):
    # return np.arange(2, HDx_max + 1) * guess_signal_bin
    hd_bins = np.arange(2, HDx_max + 1) * guess_signal_bin
    nyquist_zone = np.floor(hd_bins / (N / 2)) + 1
    K = np.floor(nyquist_zone / 2)
    hd_fold_bins = np.abs(hd_bins - K * N)
    return hd_fold_bins


# Unit Testing
if __name__ == '__main__':
    print('analysis_util')
    test_range_format = False
    test_mask = False
    test_guess_fft_signal_bin = False
    test_guess_fft_hd_bin = True

    if test_range_format == True:
        # Hold Range
        print('Hold Range')
        print('%10f %s' % (range_format(1.2345678, 'kV')))
        print('%10f %s' % (range_format(1.2345678, 'V')))
        print('%10f %s' % (range_format(1.2345678, 'mV')))
        print('%10f %s' % (range_format(1.2345678, 'uV')))
        print('%10f %s' % (range_format(1.000002345678, 'nV')))
        # Lower Range
        print('Lower Range')
        print('%10f %s' % (range_format(0.12345678, 'kV')))
        print('%10f %s' % (range_format(0.0012345678, 'V')))
        print('%10f %s' % (range_format(0.0000012345678, 'mV')))
        print('%10f %s' % (range_format(0.00000012345678, 'uV')))
        # Higher Range
        print('Higher Range')
        print('%10f %s' % (range_format(1234.5678, 'kV')))
        print('%10f %s' % (range_format(12345678, 'V')))
        print('%10f %s' % (range_format(1234567800, 'mV')))
        print('%10f %s' % (range_format(1234567800000, 'uV')))
        # Over Range
        print('Over Range')
        print('%10f %s' % (range_format(0.00012345678, 'pV')))
        print('%10f %s' % (range_format(0.00012345678, 'fV')))
        print('%10f %s' % (range_format(12345678, 'GV')))
        print('%10f %s' % (range_format(12345678, 'TV')))
        # Range String
        print('Range String')
        print('%10f %s' % (range_format(1234.5678, 'V')))
        print('%10f %s' % (range_format(1234.5678, 'W')))
        print('%10f %s' % (range_format(1234.5678, 'uV')))
        print('%10f %s' % (range_format(1234.5678, 'uW')))
        print('%10f %s' % (range_format(1234.5678, 'kHz')))
        print('%10f %s' % (range_format(1234.5678, 'Hz')))
        print('%10f %s' % (range_format(1234.5678)))
        print('%10f %s' % (range_format(0.12345678)))

    if test_mask == True:
        testT = ((0, 2), (5, 5), (10, 13))
        for r in testT:
            print('{%d,%d}' % (r[0], r[1]))

        testL = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

        print(testL)
        testL2 = mask_array(testL, testT, 99)

        print(testL)
        print(testL2)

        print(mask_bins_gen([0, 4, 12], 3, len(testL)))

        gen = mask_bins_gen([0, 4, 12], 2, len(testL))
        testL3 = mask_array(testL, gen, 0)
        print(testL3)

    if test_guess_fft_signal_bin == True:
        testL = [0, 1, 22, 5, 2, 1, 15, 19, 17, 18, 17, 15, 17, 15, 8, 0]
        print('argmax =', guess_fft_signal_bin(testL, mask_bins=()))
        print('argmax(without 0:2) =', guess_fft_signal_bin(
            testL, mask_bins=((0, 2),)))
        print('argmax(around 13) =', guess_fft_signal_bin(
            testL, prob_bin=15, prob_bin_mainlobe=7))

    if test_guess_fft_hd_bin == True:
        freq = 12.5
        fs = 2000
        N = 2000
        #freq_bin = freq / (fs / N)
        freq_bin = freq
        hd_bin = guess_fft_hd_bin(freq_bin, 9, N)
        #hd_freq = hd_bin * (fs / N)
        hd_freq = hd_bin
        # harmonic distortion in the 1st Nyquist zone
        # FREQ:  12.5 , HDFREQ:  [ 25.   37.5  50.   62.5  75.   87.5 100.  112.5]
        print('FREQ: ', freq, ', HDFREQ: ', hd_freq)
        freq = 700
        #freq_bin = freq / (fs / N)
        freq_bin = freq
        hd_bin = guess_fft_hd_bin(freq_bin, 9, N)
        #hd_freq = hd_bin * (fs / N)
        hd_freq = hd_bin
        # harmonic distortion out of 1st Nyquist zone
        # FREQ:  700 , HDFREQ:  [600. 100. 800. 500. 200. 900. 400. 300.]
        print('FREQ: ', freq, ', HDFREQ: ', hd_freq)
