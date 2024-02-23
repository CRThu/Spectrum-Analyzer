from adcmodel import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.ticker import FormatStrFormatter, MultipleLocator

FS = 10
FS_Vrms = FS / 2 / math.sqrt(2)
adc_bits = 20
histlen = 2 ** adc_bits
N = 2**28
Wave_freq = 1023.456789

Wave_Vrms = FS_Vrms * ((2 ** adc_bits) - 1) / (2 ** adc_bits) * 1.01
offset = -FS / (2 ** adc_bits) / 2

data = adcmodel(DR=90, N=N, adc_bits=adc_bits, output='code', Wave_offset=offset, FS=FS, Wave_freq=Wave_freq,
                Wave_Vrms=Wave_Vrms)

# hist
data += (histlen / 2)
data = data.astype(np.int64)
code_count_h = np.bincount(data, minlength=histlen)  # Histogram 从最小码值到最大码值做直方图,hist(x,n),z

no_value_position = np.where(code_count_h == 0)  # 丢码的位置
miss_num = np.size(no_value_position)  # 丢码的个数

print('Hist Report:')
print(f'---------------------')
print(f'hist[0]={code_count_h[0]}')
print(f'hist[1]={code_count_h[1]}')
print(f'...')
print(f'index[min]={code_count_h.argmin()}')
print(f'hist[index[min]]={code_count_h[code_count_h.argmin()]}')
print(f'len(zero(hist[]))={miss_num}')
print(f'...')
print(f'hist[-2]={code_count_h[-2]}')
print(f'hist[-1]={code_count_h[-1]}')
print(f'---------------------')

print('Saving...')
# np.savetxt('wave_gen.txt', data, fmt='%d')
data.astype(np.uint32).tofile('wave_gen.bin')

# ### GUI ###
# print('Running Plot...')
# # GUI Config
# mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# mpl.rcParams['axes.unicode_minus'] = False
# mpl.rcParams['mathtext.fontset'] = 'cm'
#
# fig = plt.figure(figsize=(8, 5))
# ax = fig.gca()
# ax.set_title('Time', fontsize=16)
# ax.set_xlabel('Samples')
# ax.set_ylabel('Voltage')
# ax.grid(True, which='both')
# ax.plot(data)
# plt.show()
#
# fig = plt.figure(figsize=(8, 5))
# ax = fig.gca()
# ax.set_title('Time', fontsize=16)
# ax.set_xlabel('Samples')
# ax.set_ylabel('Voltage')
# ax.grid(True, which='both')
# ax.plot(code_count_h)
# plt.show()
