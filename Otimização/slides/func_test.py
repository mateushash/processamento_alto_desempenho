import funcao_minima_benchmark
import numpy as np

def matrix_sum(A):
    sum = 0
    for i in range(len(A)):
        for j in range(len(A[i])):
            sum += A[i][j]
    return sum

rows = 1000
cols = 1000
A = np.random.rand(rows, cols)

resultado, median, tempos = funcao_minima_benchmark.benchmark(matrix_sum, A) 
print(f"Resultado: {resultado}")
print(f"Mediana: {median}")
print(f"Tempos: {tempos}")
