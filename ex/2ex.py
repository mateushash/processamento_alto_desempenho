from mpi4py import MPI 
import numpy as np

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
size = comm.Get_size()

n = 1000

#array = np.array([n + 1 for n in range(n)])
if rank == 0:
    dados = np.arange(1, n + 1)
    blocos_locais = np.array_split(dados, size)
else:
    blocos_locais = None

bloco_local = comm.scatter(blocos_locais, root=0)
soma_global = comm.reduce(np.sum(bloco_local), op=MPI.SUM, root=0)

if rank == 0:
    print(f"Soma global: {soma_global}")



