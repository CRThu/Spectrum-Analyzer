import numpy as np

import data_decode as dec
import fftplot as f

if __name__ == '__main__':

    fs = 50
    FS = 5
    vbias = 0

    #Zoom_fin = 0.1
    Zoom_fin = 1

    #window='HFT90D'
    window='HFT248D'

    #file = './data/AD7124_Test;SNR;FREQ;1;AMPS;400;PTS;1024;.txt'
    #file = './data/AD7124_Test;SNR;FREQ;0.1;AMPS;400;PTS;8192;.txt'
    #file = './data/AD7124_Test;SNR;FREQ;1;AMPS;40;PTS;8192;.txt'
    #file = './data/AD7124_Test;SNR;FREQ;1;AMPS;400;PTS;8192;.txt'
    #file = './data/AD7124_Test;SNR;FREQ;1;AMPS;2300;PTS;8192;.txt'
    #file = './data/AD7124_Test;SNR;FREQ;1;AMPS;4800;PTS;8192;.txt'
    file = './data/AD7124_HP;Post Filter;50SPS;Noise;.txt'
    

    adc_sample = dec.data_decode(filename=file, base='dec',
                                encode='offset', adc_bits=24, FS=FS, vbias=vbias)

    print('Data length = %d, Range = [%f,%f]' % (
        len(adc_sample), np.min(adc_sample), np.max(adc_sample)))

    f.fftplot(signal=adc_sample, fs=fs, Nomalized='dBFS', FS=FS, Window=window,
              Zoom='Part', Zoom_fin=Zoom_fin,
              HDx_max=20,
              PlotT=True, PlotSA=True, PlotSP=False)
