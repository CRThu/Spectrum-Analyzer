import math

import numpy as np

import analysis_util as util


def adcmodel(N=8192, fs=48000, FS=2.5,
             Wave='sine', Wave_freq=1000, Wave_offset=0, Wave_Vrms=0.7746,
             HDx=[],
             adc_bits=None, DR=None,
             INL=None):

    FS_Vrms = FS / 2 / math.sqrt(2)

    # Sine Wave Generate
    t = np.linspace(0, N / fs, N)

    sinout = np.empty(N)
    sinout.fill(Wave_offset)

    sinout += util.vrms2vamp(Wave_Vrms) * np.sin(2 * np.pi * Wave_freq * t + 0)

    for index in range(len(HDx)):
        sinout += util.vpp2vamp(FS * util.db2vratio(HDx[index])) * \
            np.sin(2 * np.pi * (index + 2) * Wave_freq * t + 0)

    ### ERR ###
    # Over Full Scale
    #np.clip(sinout, 0, FS/2)

    ### Noise ###
    # White Noise
    if DR is not None:
        sinout += util.wgn_dr(FS, DR, N)

    # Quantization Noise
    if adc_bits is not None:
        lsb = FS / (2 ** adc_bits)
        sinout = np.round(sinout / lsb) * lsb

    sinout -= np.mean(sinout)

    return sinout


if __name__ == "__main__":
    print('adcmodel')
    adcmodel()
