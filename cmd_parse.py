
import argparse


parser = argparse.ArgumentParser(description='test')

# shared arguments
parser.add_argument('--fullscale', dest='fullscale', type=float)

# data_decode arguments
parser.add_argument('--filepath', dest='filepath', type=str)
parser.add_argument('--split', dest='split', type=str)
parser.add_argument('--base', dest='base', type=str)
parser.add_argument('--encode', dest='encode', type=str)
parser.add_argument('--adcbits', dest='adcbits', type=int)
parser.add_argument('--vbias', dest='vbias', type=float)

# fftplot arguments
# not import: signal, spurious_existed_freqs, Wave, czt_zoom_window, czt_zoom_ratio, axes, override_print
parser.add_argument('--samplerate', dest='samplerate',type=float)
parser.add_argument('--noiseband', dest='noiseband', type=float)
parser.add_argument('--zoomcfg', dest='zoom', type=str)
parser.add_argument('--fin', dest='zoom_expfin',type=float)
parser.add_argument('--period', dest='zoom_period', type=float)
parser.add_argument('--nomalized', dest='Nomalized', type=str)
parser.add_argument('--window', dest='window', type=str)
parser.add_argument('--noisecorr', dest='noise_corr', type=bool)
parser.add_argument('--plottime', dest='PlotT', type=bool)
parser.add_argument('--plotspectrum', dest='PlotSA', type=bool)
parser.add_argument('--plotphase', dest='PlotSP', type=bool)
parser.add_argument('--hdmax', dest='HDx_max', type=int)
parser.add_argument('--impedance', dest='impedance', type=float)

args = parser.parse_args(['--hd=5', '--window=x'])
args_dict = vars(args)
print(args_dict)
