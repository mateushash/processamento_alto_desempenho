import csv
from time import perf_counter

import numpy as np


def time_benchmark(f, *args, repeat:int = 1,):
    """

    Args:
        f (): 
        *args: 

    Returns:
        
    """
    execution_times = []
    for i in range(repeat):
        t0 = perf_counter()
        # Discard the returns
        _ = f(*args)
        execution_times.append(perf_counter() - t0)
    return execution_times

def metrics(execution_times):
    min = np.min(execution_times)
    mean = np.mean(execution_times)
    median = np.median(execution_times)
    desvio_p = np.std(execution_times)
    return min, mean, median, desvio_p

def calc_speed_up(ref_times: list, execution_times: list):
    size = len(ref_times)
    speed_up = [None] * size 
    for i in range(size):
        speed_up[i] = ref_times[i] / execution_times[i]
    return speed_up



def write_benchmark_metrics(
        functions: list, 
        *args,
        element_size: list | None = None, 
        experiment_title: str = '', 
):
    """
    Write the metrics of function f to a csv file
    (Righ now only works to stencill2D)

    Args:
        functions: 
        experiment_title: 
        *args: 
    """
# TODO: Generalize to work with any f with args
    headers = ['f_name', 'size', 'min', 'mean', 'median', 'desvio_p']
    data = []
    if element_size is None:
        element_size = [500, 1000, 2000, 4000]
    results_path = "./results/"

    for size in element_size:
        # TODO: args should be defined outside of this function
        A = np.random.default_rng(seed=42).uniform(0, 1000, (size, size))
        for f in functions:
            execution_times = time_benchmark(f, A)
            min, mean, median, desvio_p = metrics(execution_times)

        data.append([f.__name__, size, min, mean, median, desvio_p])

    with open(results_path + f"resultados{experiment_title}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def call_f_for_element_size(
        element_size: list | None = None, 
):
    if element_size is None:
        element_size = [500, 1000, 2000, 4000]

    for size in element_size:
        A = np.empty((size, size), dtype=np.float64)

