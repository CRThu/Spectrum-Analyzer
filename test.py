import numpy
import timeit

a = numpy.arange(36).reshape(6, 6)

print(a)
print(a[:, 0:3])

print('timeit :', timeit.timeit(stmt=lambda: a[:, 0:3], number=1000))
print('timeit :', timeit.timeit(stmt=lambda: a[:, range(3)], number=1000))

