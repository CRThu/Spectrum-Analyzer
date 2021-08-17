import numpy
import timeit

a = numpy.arange(36).reshape(6, -1)

print(a)
print(a[:, 0:3])
mul=numpy.arange(6)
print(a*mul)
print(numpy.min(a*mul),numpy.max(a*mul))

print('timeit :', timeit.timeit(stmt=lambda: numpy.zeros(16384), number=1000))
print('timeit :', timeit.timeit(stmt=lambda: numpy.full(16384,1), number=1000))
