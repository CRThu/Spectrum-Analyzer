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


def vrms2amp(vrms):
    return (vrms * math.sqrt(2))


def vrms2vpp(vrms):
    return (vrms * math.sqrt(2) * 2)


def amp2vrms(amp):
    return (amp / math.sqrt(2))


def vpp2vrms(vpp):
    return (vpp / math.sqrt(2) / 2)

### Vamp <-> Power <-> dBm ###


def amp2power(amp, Z=600):
    return (amp / math.sqrt(2)) ** 2 / Z


def vrms2power(vrms, Z=600):
    return vrms ** 2 / Z

# 0 dBm = 1 mW
# 30 dBm = 1 W


def amp2dbm(amp, Z=600):
    return 10 * math.log10((amp / math.sqrt(2)) ** 2 / Z * 1000)


def vrms2dbm(vrms, Z=600):
    return 10 * math.log10(vrms ** 2 / Z * 1000)
