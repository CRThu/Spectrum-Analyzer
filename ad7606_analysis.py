import numpy as np

import data_decode as dec
import fftplot as f

if __name__ == '__main__':

    fs = 200000

    FS = 20 # +/-10V

    vbias = 0
    Zoom_fin = 1000

    #filename = './TestData_88d69.txt'

    path = 'D:/Files/202105毕业论文/Export/动态/'
    filename = 'File_AdDataConvert_4Lt4P_89d52'
    ext='.txt'

    adc_sample = dec.data_decode(path+filename+ext, base='hex',
                                encode='offset', adc_bits=16, FS=FS, vbias=vbias)

    f.fftplot(signal=adc_sample, fs=fs, Nomalized='dBFS', FS=FS, Window='HFT248D',
              Zoom='Part', Zoom_fin=Zoom_fin,
              HDx_max=5,
              PlotT=True, PlotSA=True, PlotSP=False)
    