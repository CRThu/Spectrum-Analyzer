import numpy as np
from scipy import signal as wd

# Window Defination and coefficients
# weight : Sequence of weighting coefficients
# CPG (Ratio)
# Mainlobe width of one side (Bins)
# All Mainlobe width : (winMainobeWidth * 2 + 1)
# NENBW (Bins)
winCoef = {
    'HFT90D' : {
        'weight' : [1, 1.942604, 1.340318, 0.440811, 0.043097],
        'CPG' : 1.000,
        'mainlobe' : 5,
        'NENBW' : 3.8832,},
    'HFT144D' : {
        'weight' : [1, 1.96760033, 1.57983607, 0.81123644, 0.22583558, 0.02773848, 0.00090360],
        'CPG' : 1.000,
        'mainlobe' : 7,
        'NENBW' : 4.5386,},
    'HFT248D' : {
        'weight' : [1, 1.985844164102, 1.791176438506, 1.282075284005, 0.667777530266, 0.240160796576, 0.056656381764, 0.008134974479, 0.000624544650, 0.000019808998, 0.000000132974],
        'CPG' : 1.000,
        'mainlobe' : 11,
        'NENBW' : 5.6512,},
}

# Generate Window with CPG Correction
def general_cosine(N, weight, CPG = 1.000, sym = True):
    return wd.windows.general_cosine(N, weight, sym = sym) * CPG

def HFT90D(N, sym = True):
    return general_cosine(N, winCoef['HFT90D']['weight'], winCoef['HFT90D']['CPG'], sym = sym)

def HFT144D(N, sym = True):
    return general_cosine(N, winCoef['HFT144D']['weight'], winCoef['HFT144D']['CPG'], sym = sym)

def HFT248D(N, sym = True):
    return general_cosine(N, winCoef['HFT248D']['weight'], winCoef['HFT248D']['CPG'], sym = sym)

def get_window(window, N, sym = True):
    return general_cosine(N, winCoef[window]['weight'], winCoef[window]['CPG'], sym = sym)

def has_window(window):
    return window in winCoef

def get_window_mainlobe_width(window):
    return winCoef[window]['mainlobe']

def get_window_NENBW(window):
    return winCoef[window]['NENBW']