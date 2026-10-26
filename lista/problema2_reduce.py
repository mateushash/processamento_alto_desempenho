from mpi4py import MPI
import numpy as np 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Sincronização inicial
comm.Barrier()
start_time = MPI.Wtime()

# ETAPA 1: Distribuição dos dados
if rank == 0:
    N = 10000003
    dados = np.arange(1, N+1)
    dados = np.array_split(dados, size)
else:
    N = None
    dados = None

dados_locais = comm.scatter(dados, root=0)

# ETAPA 2: Processamento local
soma_local = np.sum(dados_locais)
quantidade_local = len(dados_locais)

# ETAPA 3: Resultado Global
soma_global = comm.reduce(soma_local, op=MPI.SUM, root=0)
quantidade_global = comm.reduce(quantidade_local, op=MPI.SUM, root=0)

# Sincronização final
comm.Barrier()
end_time = MPI.Wtime()

execution_time = end_time - start_time
execution_time_total = comm.reduce(execution_time, op=MPI.MAX, root=0)

# ETAPA 4: Validação
if rank == 0:
    #print(f"Soma Global: {soma_global}")
    #print(f"Quantidade Global: {quantidade_global}")

    print("Tempo de execução (s):", execution_time_total)
