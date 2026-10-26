from mpi4py import MPI 
import numpy as np

def is_prime(n):
    if n <= 1:
        return False
    if n % 2 == 0 and n > 2: 
        return False 
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False

    return True

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


################ Sincronização inicial
comm.Barrier()
start_time = MPI.Wtime()
################ Sincronização inicial

N = None 

if rank == 0:
    N = 2000000

N = comm.bcast(N, root=0)

local_primos = []

for i in range(2 + rank, N, size):
    local_primos.append(i) if is_prime(i) else None

global_primos = comm.gather(local_primos, root=0)

############### Sincronização final
comm.Barrier()
end_time = MPI.Wtime()
execution_time = end_time - start_time
execution_time_total = comm.reduce(execution_time, op=MPI.MAX, root=0)
############### Sincronização final

if rank == 0:
    primos = []
    for sublist in global_primos:
        primos.extend(sublist)
#    print(f"Primos encontrados: {primos}")

    print("Tempo de execução (s):", execution_time_total)

