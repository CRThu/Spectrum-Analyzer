import re

import numpy as np


# split: \r\n,;| or others
# base: hex/dec
# encode: offset/comp
def adc_decode(filename, split='', base='hex', encode='offset',
               adc_bits=16, FS=5, offset=0):
    # Read file without blank
    with open(filename, 'r') as f:
        adc_data_strs = f.read().replace(' ', '')

    # regex split
    pattern = '\r\n,;|' + split
    adc_data_split = re.split(r'[' + pattern + ']+', adc_data_strs)

    # delete blank element
    adc_data_split = [i for i in adc_data_split if i != '']

    # base convertion
    base_num = None
    if base == 'hex':
        base_num = 16
    elif base == 'dec':
        base_num = 10
    assert base_num is not None
    adc_data = []
    for i in range(len(adc_data_split)):
        try:
            adc_data.append(int(adc_data_split[i], base_num))
        except:
            print('[ERROR]: Error in element = %d' % (i + 1))
            raise ValueError

    adc_data = np.array(adc_data, dtype='float')

    # encode
    assert encode == 'offset'
    if encode == 'offset':
        adc_data -= 2 ** (adc_bits - 1)

    # convert voltage
    adc_data *= FS / 2 ** adc_bits
    adc_data += offset
    return adc_data


if __name__ == '__main__':
    adc_decode('./TestData_88d69.txt', base='hex',
               encode='offset', adc_bits=16, FS=10, offset=0)
