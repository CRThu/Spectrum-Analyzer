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
                           adcbits=args.adcbits, fullscale=args.adcfullscale, vbias=args.adcvbias)

f.fftplot(signal=adc_data, samplerate=args.fsample,
          noiseband=None, spurious_existed_freqs=((),),
          Wave='Raw',
          zoom='All', zoom_expfin=None, zoom_period=3,
          nomalized='dBFS',
          fullscale=args.adcfullscale,
          window=args.window,
          czt_zoom_window='blackmanharris', czt_zoom_ratio=10,
          noise_corr=True,
          PlotT=args.plottime, PlotSA=args.plotmag, PlotSP=args.plotphase,
          HDx_max=args.hdmax,
          impedance=600)
