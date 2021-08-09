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


# [{argv, dest, type, help}, ...]
ARGVS_LIST = [
    {'argv': '--fullscale', 'dest': 'fullscale', 'type': float,
        'help': 'ADC full scale voltage (V), fullscale of ±5V ADC is 10V'},
    {'argv': '--filepath', 'dest': 'filepath', 'type': str,
        'help': 'file path, don\'t give this param if using GUI'},
    {'argv': '--split', 'dest': 'split', 'type': str,
        'help': 'char for data decode in file, default chars: \'\\r\\n,;|\''},
    {'argv': '--base', 'dest': 'base', 'type': str,
        'help': 'base of number for data decode in file, choose: \'hex\' or \'dec\''},
    {'argv': '--encode', 'dest': 'encode', 'type': str,
        'help': 'encode of number for data decode in file, choose: \'offset\' or \'comp\''},
    {'argv': '--adcbits', 'dest': 'adcbits', 'type': int, 'help': 'ADC bits'},
    {'argv': '--vbias', 'dest': 'vbias', 'type': float,
        'help': 'ADC Vbias Voltage (V)'},
    {'argv': '--samplerate', 'dest': 'samplerate',
        'type': float, 'help': 'ADC sample rate (Hz)'},
    {'argv': '--noiseband', 'dest': 'noiseband', 'type': float,
        'help': 'ADC noise band for calculate (Hz)'},
    {'argv': '--zoom', 'dest': 'zoom', 'type': str,
        'help': 'zoom at time domain plot, choose: \'All\' or  \'Part\''},
    {'argv': '--fin', 'dest': 'zoom_expfin', 'type': float,
        'help': 'rough frequency for zoom at time domain plot (Hz)'},
    {'argv': '--period', 'dest': 'zoom_period', 'type': float,
        'help': 'periods for zoom at time domain plot'},
    {'argv': '--nomalized', 'dest': 'nomalized', 'type': str,
        'help': 'nomalized convertion, choose: \'dBFS\' or \'dBm\''},
    {'argv': '--window', 'dest': 'window', 'type': str,
        'help': 'window name, recommand: \'HFT90D\' and \'HFT248D\''},
    {'argv': '--noisecorr', 'dest': 'noise_corr', 'type': str2bool,
        'help': 'correction for noise, choose \'true\' or \'false\''},
    {'argv': '--plottime', 'dest': 'PlotT', 'type': str2bool,
        'help': 'display time domain plot, choose \'true\' or \'false\''},
    {'argv': '--plotspectrum', 'dest': 'PlotSA', 'type': str2bool,
        'help': 'display spectrum domain plot, choose \'true\' or \'false\''},
    {'argv': '--plotphase', 'dest': 'PlotSP', 'type': str2bool,
        'help': 'display phase spectrum domain plot, choose \'true\' or \'false\''},
    {'argv': '--hdmax', 'dest': 'HDx_max', 'type': int,
        'help': 'stages of harmonic distortion'},
    {'argv': '--impedance', 'dest': 'impedance',
        'type': float, 'help': 'impedance (R)'},
]


def cmd_parse(argvs: str = None, remove_none=True):
    parser = argparse.ArgumentParser(description='Parse Function')

    for arginfo in ARGVS_LIST:
        parser.add_argument(arginfo['argv'], dest=arginfo['dest'], type=arginfo['type'], help=arginfo['help']
                            if 'help' in arginfo and arginfo['help'] is not None else 'No help info here.')

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