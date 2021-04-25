import numpy as np
import math

def wgn(x, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(x ** 2) / len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)

def db2vratio(db):
    return math.pow(10, db / 20)

def vratio2db(ratio):
    return 20 * math.log10(ratio)

def db2pratio(db):
    return math.pow(10, db / 10)

def pratio2db(ratio):
    return 10 * math.log10(ratio)

def vrms2amp(vrms):
    return (vrms * math.sqrt(2))

def vrms2vpp(vrms):
    return (vrms * math.sqrt(2) * 2)

# numpy
def db2vratio_np(db):
    return np.power(10, db / 20)

def vratio2db_np(ratio):
    return 20 * np.log10(ratio)

def db2pratio_np(db):
    return np.power(10, db / 10)

def pratio2db_np(ratio):
    return 10 * np.log10(ratio)