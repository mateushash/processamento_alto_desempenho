from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

################ Sincronização inicial
comm.Barrier()
start_time = MPI.Wtime()
################ Sincronização inicial

if rank == 0:
    N = 100000000
    x = np.linspace(-1, 1, N)
    y = np.linspace(-1, 1, N)
else:
    N = None
    x = None
    y = None
    circle = None

N = comm.bcast(N, root=0)

seed = 10 + rank  # Semente diferente para cada processo
np.random.seed(seed)

local_points = np.random.rand(N // size, 2) * 2 - 1  # Gera pontos aleatórios no quadrado [-1, 1] x [-1, 1]
local_circle = [point for point in local_points if point[0]**2 + point[1]**2 <= 1]

global_circle = comm.reduce(len(local_circle), op=MPI.SUM, root=0)
global_points = comm.reduce(len(local_points), op=MPI.SUM, root=0)

############### Sincronização final
comm.Barrier()
end_time = MPI.Wtime()
execution_time = end_time - start_time
execution_time_total = comm.reduce(execution_time, op=MPI.MAX, root=0)
############### Sincronização final

if rank == 0:
    pi_estimate = 4 * global_circle / global_points
    print(f"Estimated value of pi: {pi_estimate}")
    print("Tempo de execução (s):", execution_time_total)

