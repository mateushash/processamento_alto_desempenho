from mpi4py import MPI
import numpy as np 

comm = MPI.COMM_WORLD 
rank = comm.Get_rank() 
size = comm.Get_size()

if rank == 0: 
    n = 100000000
    dados = np.linspace(0, 1, n)
    dados_locais = np.array_split(dados, size)
else:
    n = None
    dados = None
    dados_locais = None


n = comm.bcast(n, root=0)
dado_local = comm.scatter(dados_locais, root=0) 
delta = 1.0 / n

pi_local = (4/(1 + dado**2) * delta for dado in dado_local)

pi_global = comm.reduce(sum(pi_local), op=MPI.SUM, root=0)

if rank == 0:
    print(f"Valor aproximado de pi: {pi_global}")

