import math
import random

import numpy as np

import analysis_util as util


def adcmodel(samplesnum=1, **kwargs):
    if samplesnum == 1:
        # 1-D Numpy array
        return adcmodel_gensample(**kwargs)
    else:
        # 2-D Numpy array
        return np.array([adcmodel_gensample(**kwargs) for _ in range(samplesnum)])

def adcmodel_gensample(N=8192, fs=48000, FS=2.5,
                       Wave='sine', Wave_freq=1000, Wave_offset=0, Wave_Vrms=0.7746,
                       Wave_phase=None,
                       HDx=[],
                       adc_bits=None, DR=None,
                       INL=None):

    FS_Vrms = FS / 2 / math.sqrt(2)

    # Sine Wave Generate
    t = np.linspace(0, N / fs, N)

    sinout = np.full(N, fill_value=Wave_offset, dtype=np.float64)

    if Wave_phase is None:
        Wave_phase = random.uniform(-np.pi, np.pi)
    sinout += util.vrms2vamp(Wave_Vrms) * np.sin(2 * np.pi * Wave_freq * t + Wave_phase)

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
    data = adcmodel(DR=100)
    print(data.dtype, data.shape)
    data = adcmodel(DR=100, samplesnum=4)
    print(data.dtype, data.shape)
