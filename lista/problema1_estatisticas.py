from mpi4py import MPI
import numpy as np 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ETAPA 1: Distribuição dos dados
if rank == 0:
    N = 10000003
    dados = np.random.random(N)
    dados = np.array_split(dados, size)
else:
    N = None
    dados = None

N = comm.bcast(N, root=0)
dados_locais = comm.scatter(dados, root=0)

# ETAPA 2: Processamento local
soma_local = np.sum(dados_locais)
quantidade_local = len(dados_locais)
maximo_local = np.max(dados_locais)
minimo_local = np.min(dados_locais)

# ETAPA 3: Resultado Global
soma_global = comm.reduce(soma_local, op=MPI.SUM, root=0)
quantidade_global = comm.reduce(quantidade_local, op=MPI.SUM, root=0)
max_global = comm.reduce(maximo_local, op=MPI.MAX, root=0)
min_global = comm.reduce(minimo_local, op=MPI.MIN, root=0)

# ETAPA 4: Validação
if rank == 0:
    media = soma_global / quantidade_global,

    print(f"Soma Global: {soma_global}")
    print(f"Quantidade Global: {quantidade_global}")
    print(f"Média: {media}")
    print(f"Máximo Global: {max_global}")
    print(f"Mínimo Global: {min_global}")

    print("\nValidação com numpy:\n")
    print(f"Soma Global (numpy): {np.sum(np.concatenate(dados))}")
    print(f"Quantidade Global (numpy): {len(np.concatenate(dados))}")
    print(f"Média (numpy): {np.mean(np.concatenate(dados))}")
    print(f"Máximo Global (numpy): {np.max(np.concatenate(dados))}")
    print(f"Mínimo Global (numpy): {np.min(np.concatenate(dados))}")

