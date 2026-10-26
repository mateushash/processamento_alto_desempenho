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
#     display_name: ai_python
#     language: python
#     name: ai_python
# ---

# %%
# Funcao minima benchmark
from time import perf_counter
from statistics import median
import tracemalloc
import numpy as np

def benchmark(func, *args, repeat=9):
    tempos = []
    resultado = None
    for _ in range(repeat):
        t0 = perf_counter()
        resultado = func(*args)
        tempos.append(perf_counter() - t0)
    return resultado, median(tempos), tempos

# %%
# Funcao test
def matrix_sum(A):
    sum = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            sum += A[i][j]
    return sum

rows = 1000
cols = 1000
A = np.random.rand(rows, cols)

# %%
benchmark(matrix_sum, A) 

# %%
# Versao A: recalcula uma constante n vezes 
def versao_a(x, a, b):
    s = 0.0 
    for xi in x:
        s += xi * ((a**2 + b**2) ** 0.5)
    return s 

# %%
# Versao B: hoisting - move o invariante pra fora do laço 
def versao_b(x, a, b):
    c = (a**2 + b**2) ** 0.5
    s = 0.0
    for xi in x:
        s += xi * c 
    return s

# %%
a = 10 
b = 100 
x = np.random.rand(1000000)

# %%
benchmark(versao_a, x, a, b)

# %%
benchmark(versao_b, x, a, b)

# %%
# Estrutura de dados altera o custo da busca
import random

dados = list(range(1_000_000))
consultas = [random.randrange(1_200_000) for _ in range(50_000)]

def busca_lista(dados, consultas):
    return sum(q in dados for q in consultas)

def busca_set(dados, consultas):
    indice = set(dados)
    return sum(q in indice for q in consultas)

# %%
benchmark(busca_lista, dados, consultas)

# %%
benchmark(busca_set, dados, consultas)

# %%
# 4 - microbenchmarkd de overhead de chamada
def quadrado(x):
    return x * x 

def com_chamada(n):
    s = 0 
    for i in range(n):
        s += quadrado(i)
    return s 

def inline(n):
    s = 0 
    for i in range(n):
        s += i*i 
    return s

# %%
benchmark(com_chamada, 100000)

# %%
benchmark(inline, 100000)


# %%
# pre alocacao 
def benchmark_memo(func, *args, repeat=9):
    tempos = []
    for _ in range(repeat):
        tracemalloc.start()
        _= func(*args)
        tempos.append(perf_counter() - t0)
#    return resultado, median(tempos), tempos
    return median(tempos), tempos


def preencher_lista(n):
    y = []
    for i in range(n):
        y.append(i * i)
    return y 

def preencher_array(n):
    y = np.empty(n, dtype=np.int64)
    for i in range(n):
        y[i] = i * i 
    return y


# %%
benchmark(preencher_lista, 100_000)

# %%
benchmark(preencher_array, 100_000)
