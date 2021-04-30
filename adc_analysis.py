import numpy as np

import adc_decode as dec
import fftplot as f

if __name__ == '__main__':

    fs = 200000
    fbase = 925.000
    FS=10
    offset=0

    adc_sample = dec.adc_decode('./TestData_88d69.txt', base='hex',
                                encode='offset', adc_bits=16, FS=10, offset=0)
    
    f.fftplot(signal=adc_sample, fs=fs, fbase=fbase, Nomalized='dBFS', FS=FS, Window='HFT248D',
            Zoom='Part', Zoom_fin=fbase,
            PlotT=True, PlotSA=True, PlotSP=False)
