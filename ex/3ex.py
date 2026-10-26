from mpi4py import MPI 
import numpy as np 

comm = MPI.COMM_WORLD 
rank = comm.Get_rank() 

if rank == 0:
    dados = np.random.randint(1000001, size=1000000)  # Gera um array de 1 milhão de números aleatórios entre 0 e 1.000.000
    blocos_locais = np.array_split(dados, comm.Get_size())
else:
    blocos_locais = None
    dados = None

bloco_local = comm.scatter(blocos_locais, root=0)
max_local = np.max(bloco_local)

max_global = comm.reduce(max_local, op=MPI.MAX, root=0)

if rank == 0:
    print(f"Máximo global: {max_global}")
    print(f"Máximo global (usando numpy): {np.max(dados)}")


