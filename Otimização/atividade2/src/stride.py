from time import perf_counter

import numpy as np

import csv


def test_stride(intervals: list[int],
        experiment_title: str = 'Stride', 
        ):
    N = 50_000_000
    A = np.ones(N, dtype=np.float64)
    headers = ['stride', 'acessos', 'tempo_de_acesso', 'tempo_por_acesso']
    results = []
    results_path = "./results/"
    
    for stride in intervals:
        t0 = perf_counter() 
        A[::stride]
        dt = perf_counter() - t0 
        acessos = (N + stride - 1) // stride
        t_by_acesso = dt / acessos
        
        results.append((stride, acessos, dt, t_by_acesso))

    with open(results_path + f"resultados{experiment_title}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(results)



