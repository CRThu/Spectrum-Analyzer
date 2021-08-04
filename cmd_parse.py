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


# [(argv, dest, type, help), ...]
ARGVS_TUPLE = [
    ('--fullscale', 'fullscale', float, 'ADC full scale voltage (V), fullscale of ±5V ADC is 10V'),
    ('--filepath', 'filepath', str, 'file path, don\'t give this param if using GUI'),
    ('--split', 'split', str, 'char for data decode in file, default chars: \'\\r\\n,;|\''),
    ('--base', 'base', str, 'base of number for data decode in file, choose: \'hex\' or \'dec\''),
    ('--encode', 'encode', str,'encode of number for data decode in file, choose: \'offset\' or \'comp\''),
    ('--adcbits', 'adcbits', int,'ADC bits'),
    ('--vbias', 'vbias', float,'ADC Vbias Voltage (V)'),
    ('--samplerate', 'samplerate', float,'ADC sample rate (Hz)'),
    ('--noiseband', 'noiseband', float,'ADC noise band for calculate (Hz)'),
    ('--zoom', 'zoom', str,'zoom at time domain plot, choose: \'All\' or  \'Part\''),
    ('--fin', 'zoom_expfin', float,'rough frequency for zoom at time domain plot (Hz)'),
    ('--period', 'zoom_period', float,'periods for zoom at time domain plot'),
    ('--nomalized', 'nomalized', str,'nomalized convertion, choose: \'dBFS\' or \'dBm\''),
    ('--window', 'window', str,'window name, recommand: \'HFT90D\' and \'HFT248D\''),
    ('--noisecorr', 'noise_corr', str2bool,'correction for noise, choose \'true\' or \'false\''),
    ('--plottime', 'PlotT', str2bool,'display time domain plot, choose \'true\' or \'false\''),
    ('--plotspectrum', 'PlotSA', str2bool,'display spectrum domain plot, choose \'true\' or \'false\''),
    ('--plotphase', 'PlotSP', str2bool,'display phase spectrum domain plot, choose \'true\' or \'false\''),
    ('--hdmax', 'HDx_max', int,'stages of harmonic distortion'),
    ('--impedance', 'impedance', float,'impedance (R)')
]


def cmd_parse(argvs: str = None, remove_none=True):
    parser = argparse.ArgumentParser(description='Parse Function')

    for arginfo in ARGVS_TUPLE:
        parser.add_argument(arginfo[0], dest=arginfo[1], type=arginfo[2], help=arginfo[3] if len(
            arginfo) == 4 and arginfo[3] is not None else 'No help info here.')

    if argvs is None:
        args = parser.parse_args()
    else:
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


if __name__ == '__main__':
    cmd_parse('-h')
