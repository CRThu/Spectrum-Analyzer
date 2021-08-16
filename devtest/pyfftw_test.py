from numpy.ma.core import array
import pyfftw
import multiprocessing
import scipy.fft
import scipy.fftpack
import numpy.fft
import timeit

# https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.fft.html
# https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html#numpy.fft.fft
# https://pyfftw.readthedocs.io/en/latest/source/tutorial.html

iternum=1
#a = numpy.random.rand(256, 8192)
a = numpy.random.rand(100, 65536)
#a = numpy.random.rand(32, 1048576)


print('Time with numpy backend: %1.3f seconds' %
      timeit.timeit(stmt=lambda: numpy.fft.fft(a), number=iternum))
print('Time with scipy fft backend: %1.3f seconds' %
      timeit.timeit(stmt=lambda: scipy.fft.fft(a), number=iternum))


# Configure PyFFTW to use all cores (the default is single-threaded)
#pyfftw.config.NUM_THREADS = multiprocessing.cpu_count()

# Use the backend pyfftw.interfaces.scipy_fft
with scipy.fft.set_backend(pyfftw.interfaces.scipy_fft):
    # Turn on the cache for optimum performance
    #pyfftw.interfaces.cache.enable()

    print('Time with scipy+pyfftw backend: %1.3f seconds' %
          timeit.timeit(stmt=lambda: scipy.fft.fft(a), number=iternum))
