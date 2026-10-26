from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ETAPA 1: Distribuição dos dados
if rank == 0:
    N = 100000000
    b = np.pi
    a = 0.0
else:
    N = None
    b = None
    a = None

N = comm.bcast(N, root=0)
b = comm.bcast(b, root=0)
a = comm.bcast(a, root=0)

# ETAPA 2: Processamento local

indice_locais = [i for i in range(rank, N, size)]
delta_x = (b - a) / N
integral_local = sum(np.sin(a + (i + 0.5) * delta_x) * delta_x for i in indice_locais)

# ETAPA 3: Resultado Global
integral_global = comm.reduce(integral_local, op=MPI.SUM, root=0)

# ETAPA 4: Validação
if rank == 0:
    print(f"Integral Global: {integral_global}")
