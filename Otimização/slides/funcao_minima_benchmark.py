from time import perf_counter
from statistics import median
import numpy as np

def benchmark(func, *args, repeat=9):
    tempos = []
    resultado = np.empty(repeat)
    for _ in range(repeat):
        t0 = perf_counter()
        resultado[_] = func(*args)
        tempos.append(perf_counter() - t0)
    return resultado, median(tempos), tempos
