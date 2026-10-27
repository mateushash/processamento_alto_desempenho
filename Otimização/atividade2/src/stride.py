from time import perf_counter

import numpy as np


def test_stride():
    N = 50_000_000
    A = np.ones(N, dtype=np.float64)
    results = []
    
    for stride in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        t0 = perf_counter() 
        A[::stride]
        dt = perf_counter() - t0 
        acessos = (N + stride - 1) // stride
        
        print(stride, dt, dt/acessos * 1e9, 'ns/acesso')
