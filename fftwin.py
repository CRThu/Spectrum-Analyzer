import numpy as np
from scipy import signal as wd

winCoff = {
    'HFT90D' : [1, 1.942604, 1.340318, 0.440811, 0.043097],
    'HFT144D' : [1, 1.96760033, 1.57983607, 0.81123644, 0.22583558, 0.02773848, 0.00090360],
    'HFT248D' : [1, 1.985844164102, 1.791176438506, 1.282075284005, 0.667777530266, 0.240160796576, 0.056656381764, 0.008134974479, 0.000624544650, 0.000019808998, 0.000000132974],
}

# Mainlobe width of one side
# All Mainlobe width is (winMainobeWidth * 2 + 1)
winMainobeWidth = {
    'HFT90D' : 5,
    'HFT144D' : 7,
    'HFT248D' : 11,
}

def get_windows(windows, N, sym = True):
    return wd.windows.general_cosine(N, winCoff[windows], sym = sym)

def HFT90D(N, sym = True):
    return wd.windows.general_cosine(N, winCoff['HFT90D'], sym = sym)

def HFT144D(N, sym = True):
    return wd.windows.general_cosine(N, winCoff['HFT144D'], sym = sym)

def HFT248D(N, sym = True):
    return wd.windows.general_cosine(N, winCoff['HFT248D'], sym = sym)

def get_windows_mainlobe_width(windows):
    return winMainobeWidth[windows]