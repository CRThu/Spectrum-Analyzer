import numpy as np
import math


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


# Unit Testing
if __name__ == '__main__':
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
