import numpy as np

import adc_decode as dec
import fftplot as f

if __name__ == '__main__':

    fs = 200000
    FS = 10
    offset = 0
    Zoom_fin = 1000

    adc_sample = dec.adc_decode('./TestData_88d69.txt', base='hex',
                                encode='offset', adc_bits=16, FS=10, offset=0)

    f.fftplot(signal=adc_sample, fs=fs, Nomalized='dBFS', FS=FS, Window='HFT248D',
              Zoom='Part', Zoom_fin=Zoom_fin,
              HDx_max=5,
              PlotT=True, PlotSA=True, PlotSP=False)
    