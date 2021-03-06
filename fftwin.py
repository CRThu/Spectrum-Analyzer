import numpy as np
from scipy import signal as wd

# Window Defination and coefficients
# weight : Sequence of weighting coefficients
# CPG (Ratio)
# Mainlobe width of one side (Bins)
# All Mainlobe width : (winMainobeWidth * 2 + 1)
# ENBW (Bins)
# Window Reference: https://holometer.fnal.gov/GH_FFT.pdf

# TODO Nuttall3/4 window CPG need to be calculated
winCoef = {
    'rectangle': {
        'type': 'linear',
        'CPG': 1,
        'mainlobe': 1,
        'ENBW': 1.0000, },
    'blackmanharris': {
        'type': 'cosine',
        'weight': [0.35875, 0.48829, 0.14128, 0.01168],
        'CPG': 2.787,
        'mainlobe': 4,
        'ENBW': 2.0044, },
    'nuttall3': {
        'type': 'cosine',
        'weight': [0.375, 0.5, 0.125],
        'CPG': 1,
        'mainlobe': 3,
        'ENBW': 1.9444, },
    'nuttall4': {
        'type': 'cosine',
        'weight': [0.3125, 0.46875, 0.1875,0.03125],
        'CPG': 1,
        'mainlobe': 4,
        'ENBW': 2.3100, },
    'HFT90D': {
        'type': 'cosine',
        'weight': [1, 1.942604, 1.340318, 0.440811, 0.043097],
        'CPG': 1.000,
        'mainlobe': 5,
        'ENBW': 3.8832, },
    'HFT144D': {
        'type': 'cosine',
        'weight': [1, 1.96760033, 1.57983607, 0.81123644,
                   0.22583558, 0.02773848, 0.00090360],
        'CPG': 1.000,
        'mainlobe': 7,
        'ENBW': 4.5386, },
    'HFT248D': {
        'type': 'cosine',
        'weight': [1, 1.985844164102, 1.791176438506, 1.282075284005,
                   0.667777530266, 0.240160796576, 0.056656381764, 0.008134974479,
                   0.000624544650, 0.000019808998, 0.000000132974],
        'CPG': 1.000,
        'mainlobe': 11,
        'ENBW': 5.6512, },
}


def general_cosine(N, weight, CPG=1.000, sym=True):
    return wd.windows.general_cosine(N, weight, sym=sym) * CPG

def rectangle(N):
    return [1] * N

def blackmanharris(N, sym=True):
    return general_cosine(N, winCoef['blackmanharris']['weight'], winCoef['blackmanharris']['CPG'], sym=sym)


def HFT90D(N, sym=True):
    return general_cosine(N, winCoef['HFT90D']['weight'], winCoef['HFT90D']['CPG'], sym=sym)


def HFT144D(N, sym=True):
    return general_cosine(N, winCoef['HFT144D']['weight'], winCoef['HFT144D']['CPG'], sym=sym)


def HFT248D(N, sym=True):
    return general_cosine(N, winCoef['HFT248D']['weight'], winCoef['HFT248D']['CPG'], sym=sym)


def get_window(window, N, sym=True):
    if has_window(window):
        if winCoef[window]['type'] == 'cosine':
            return general_cosine(N, winCoef[window]['weight'], winCoef[window]['CPG'], sym=sym)
        elif winCoef[window]['type'] == 'linear':
            if window == 'rectangle':
                return rectangle(N)


def has_window(window):
    return window in winCoef


def get_window_mainlobe_width(window):
    if has_window(window):
        return winCoef[window]['mainlobe']


def get_window_ENBW(window):
    if has_window(window):
        return winCoef[window]['ENBW']
