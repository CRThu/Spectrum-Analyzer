import numpy as np

import data_decode as dec
import fftplot as f

if __name__ == '__main__':

    fs = 200000

    FS = 10  # +/-10V

    vbias = 0
    Zoom_fin = 1000

    path = './data/'
    filename = 'AD7606_TestData_88d69'
    ext = '.txt'

    # path = 'D:/Files/202105毕业论文/Export/动态/'
    # filename = 'File_AdDataConvert_4Lt4P_89d52'
    # ext = '.txt'

    adc_sample = dec.data_decode(path + filename + ext, base='hex',
                                 encode='offset', adcbits=16, fullscale=FS, vbias=vbias)

    f.fftplot(signal=adc_sample, samplerate=fs, Nomalized='dBFS', fullscale=FS, window='HFT248D',
              zoom='Part', zoom_expfin=Zoom_fin,
              HDx_max=5,
              PlotT=True, PlotSA=True, PlotSP=False)
