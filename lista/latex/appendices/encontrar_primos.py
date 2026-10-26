from mpi4py import MPI 
import sys

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
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

N = comm.bcast(N, root=0)

local_primos = []

# use ciclical distribution ignoring even numbers
#P0 -> 3, 11, 19, 27, ...
#P1 -> 5, 13, 21, 29, ...
#P2 -> 7, 15, 23, 31, ...
#P3 -> 9, 17, 25, 33, ...
for i in range(3 + rank*2, N, size*2):
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

