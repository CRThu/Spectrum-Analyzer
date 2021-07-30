from cmd_parse import DATA_DECODE_ARGS, FFTPLOT_ARGS, args_filter, cmd_parse

import data_decode as dec
import fftplot as f

argvs_dict = cmd_parse()

data_decode_kwargs = args_filter(argvs_dict, DATA_DECODE_ARGS)
adc_sample = dec.data_decode(**data_decode_kwargs)

fftplot_kwargs = args_filter(argvs_dict, FFTPLOT_ARGS)
f.fftplot(signal=adc_sample, **fftplot_kwargs)
