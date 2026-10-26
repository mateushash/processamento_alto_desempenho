# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: Conda ai_env
#     language: python
#     name: ai_env
# ---

# %%
import numpy as np 
from time import perf_counter
from numba import njit

# %%
# L2 cache - 16Mb
N = 17_000_000
x = np.ones(N, dtype=np.float64)

@njit
def soma_stride(x, stride):
    s = 0.0
    for i in range(0, x.size, stride):
        s += x[i]
    return s

# %%
for stride in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
    t0 = perf_counter() 
    s = soma_stride(x, stride)
    dt = perf_counter() - t0 
    acessos = (N + stride - 1) // stride
    print(stride, dt, dt/acessos * 1e9, 'ns/acesso', s)

# %%
# L2 cache - 16Mb
N = 3000
A = np.random.random((N,N))

def soma_linhas(A):
    s = 0.0 
    n, m = A.shape
    for i in range(n):
        for j in range(m):
            s += A[i,j]

    return s

def soma_colunas(A):
    s = 0.0
    n, m = A.shape 
    for j in range(m):
        for i in range(n):
            s += A[i, j]

    return s

# %%
for f in (soma_linhas, soma_colunas):
    t0 = perf_counter()
    r = f(A)
    print(f.__name__, perf_counter() - t0, r)


# %%
for mib in [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256]:
    n = int(mib * 1024**2 / 8)
    x = np.ones(n, dtype=np.float64)

    _ = x.sum()

    tempos = []
    for _ in range(7):
        t0 = perf_counter()
        r = x.sum()
        tempos.append(perf_counter() - t0)

    med = np.median(tempos)
    print(f'{mib:7.2f} Mib {med*1e3:8.3f} ms {med/n*1e9:8.3f} ns/elem')

# %%
import tracemalloc

def medir(func, *args):
    tracemalloc.start()
    t0 = perf_counter()
    result = func(*args)
    dt = perf_counter() - t0
    atual, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, dt, pico / 1024**2
# resultado, tempo, pico_mib = medir(minha_funcao, entrada)

# %%
@njit
def soma_linhas_jit(A):
    s = 0.0
    n, m = A.shape
    for i in range(n):
        for j in range(m):
            s += A[i, j]
    return s

@njit
def soma_colunas_jit(A):
    s = 0.0
    n, m = A.shape
    for j in range(m):
        for i in range(n):
            s += A[i, j]
    return s

# %%
for f in (soma_linhas_jit, soma_colunas_jit):
    t0 = perf_counter()
    r = f(A)
    print(f.__name__, perf_counter() - t0, r)

# %%
