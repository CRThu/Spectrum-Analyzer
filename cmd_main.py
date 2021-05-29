import argparse

from numpy import double

import data_decode as dec
import fftplot as f

parser = argparse.ArgumentParser(description='Spectrum Analyzer')

# plot
parser.add_argument('-pt', '--plottime', type=bool,
                    default=False, help='plot time domain')
parser.add_argument('-pm', '--plotmag', type=bool,
                    default=True, help='plot freq mag domain')
parser.add_argument('-pp', '--plotphase', type=bool,
                    default=False, help='plot freq phase domain')

args = parser.parse_args()

adc_data = dec.data_decode(args.datafilename, split=args.datasplit,
                           base=args.decodebase, encode='offset',
                           adc_bits=args.adcbits, FS=args.adcfullscale, vbias=args.adcvbias)

f.fftplot(signal=adc_data, fs=args.fsample,
          noise_band=None, spurious_existed_freqs=((),),
          Wave='Raw',
          Zoom='All', Zoom_fin=None, Zoom_period=3,
          Nomalized='dBFS',
          FS=args.adcfullscale,
          Window=args.window,
          czt_zoom_window='blackmanharris', czt_zoom_ratio=10,
          Noise_corr=True,
          PlotT=args.plottime, PlotSA=args.plotmag, PlotSP=args.plotphase,
          HDx_max=args.hdmax,
          dBm_Z=600)
