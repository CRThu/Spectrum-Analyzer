import argparse

from numpy import double

parser = argparse.ArgumentParser(description='Spectrum Analyzer')

# data decode
parser.add_argument('-f', '--datafilename', type=str,
                    required=True, help='data decode filename')
parser.add_argument('-ds', '--datasplit', type=str, default='',
                    help='data decode file split chars')
parser.add_argument('-db', '--decodebase', type=str, required=True,
                    help='data decode data base, choose: hex or dec')

# adc info
parser.add_argument('-b', '--adcbits', type=int,
                    required=True, help='adc bits')
parser.add_argument('-fc', '--adcfullscale', type=double, required=True,
                    help='adc full scale, such as: FS=10V (-5V~+5V)')
parser.add_argument('-vb', '--adcvbias', type=double, default=0,
                    help='adc vbias voltage')

# fft
parser.add_argument('-fs', '--fsample', type=double,
                    required=True, help='adc sample rate')
parser.add_argument('-w', '--window', type=str, default='HFT248D',
                    help='fft window, recommand: HFT90D, HFT248D')

# analysis
parser.add_argument('-hd', '--hdmax', type=int, default='9',
                    help='harmonic distortion max stages')

# plot
parser.add_argument('-pt', '--plottime', type=bool,
                    default='False', help='plot time domain')
parser.add_argument('-pm', '--plotmag', type=bool,
                    default='True', help='plot freq mag domain')
parser.add_argument('-pp', '--plotphase', type=bool,
                    default='False', help='plot freq phase domain')

args = parser.parse_args()


print(args.datafilename, args.decodebase)

print(args.adcbits, args.adcfullscale, args.adcvbias)
