import numpy as np
import math
import analysis_util

def adcmodel(N = 8192, fs = 48000, FS = 2.5,
    Wave = 'sine', Wave_freq = 1000, Wave_offset = 0,
    adc_bits = None, DR = None,
    THD = None, INL = None):

    FS_Vrms = FS / 2 / math.sqrt(2)
    
    # Wave Info
    dc = Wave_offset
    fsin_base = Wave_freq
    fh2 = -106
    fh3 = -100
    fsin = [fsin_base, 2 * fsin_base, 3 * fsin_base]
    Vrms = [FS_Vrms, math.pow(10, fh2 / 20) * FS_Vrms, math.pow(10, fh3 / 20) * FS_Vrms]
    phase = [0, 0.5 * math.pi, 0.25 * math.pi]
    t = np.linspace(0, N/fs, N)

    # Sine Wave Generate
    sinout = np.empty(N)
    sinout.fill(dc)
    for index in range(len(Vrms)):
        sinout += (Vrms[index] * math.sqrt(2)) * np.sin(2 * np.pi * fsin[index] * t + phase[index])
    
    ### ERR ###
    # Over Full Scale
    #np.clip(sinout, 0, FS/2)

    ### Noise ###
    # Quantization Noise
    if adc_bits is not None:
        lsb = FS / 2 ** adc_bits
        sinout = np.round(sinout / lsb) * lsb

    sinout -= np.mean(sinout)

    return sinout

if __name__ == "__main__":
    print('adcmodel')
    adcmodel()