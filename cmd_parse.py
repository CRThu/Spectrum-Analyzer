import argparse

DATA_DECODE_ARGS = ['filepath', 'split', 'base',
                    'encode', 'adcbits', 'fullscale', 'vbias']

FFTPLOT_ARGS = ['samplerate', 'noiseband', 'zoom', 'zoom_expfin',
                 'zoom_period', 'nomalized', 'fullscale', 'window', 'noise_corr', 'PlotT', 'PlotSA', 'PlotSP', 'HDx_max', 'impedance']

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def cmd_parse(argvs: str, remove_none=True):
    parser = argparse.ArgumentParser(description='cmd parse')

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
    parser.add_argument('--samplerate', dest='samplerate', type=float)
    parser.add_argument('--noiseband', dest='noiseband', type=float)
    parser.add_argument('--zoom', dest='zoom', type=str)
    parser.add_argument('--fin', dest='zoom_expfin', type=float)
    parser.add_argument('--period', dest='zoom_period', type=float)
    parser.add_argument('--nomalized', dest='nomalized', type=str)
    parser.add_argument('--window', dest='window', type=str)
    parser.add_argument('--noisecorr', dest='noise_corr', type=str2bool)
    parser.add_argument('--plottime', dest='PlotT', type=str2bool)
    parser.add_argument('--plotspectrum', dest='PlotSA', type=str2bool)
    parser.add_argument('--plotphase', dest='PlotSP', type=str2bool)
    parser.add_argument('--hdmax', dest='HDx_max', type=int)
    parser.add_argument('--impedance', dest='impedance', type=float)

    args = parser.parse_args(argvs.split())
    args_dict = vars(args)

    if remove_none:
        for k in list(args_dict.keys()):
            if args_dict[k] is None:
                del args_dict[k]
    return args_dict

def args_filter(args: dict, kwl: list):
    argsf = dict()
    for kw in kwl:
        if kw in args:
            argsf[kw] = args[kw]
    return argsf
