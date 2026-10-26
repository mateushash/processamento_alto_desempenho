from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    dados = np.arange(1, 1001) # Cria um array de 1 a 1000
    blocos = np.array_split(dados, size) # Divide os dados em blocos iguais
else:
    blocos = None

bloco = comm.scatter(blocos, root=0) # Distribui os blocos para todos os processos
soma_local = np.sum(bloco ** 2) # Calcula a soma local do bloco

soma_global = comm.reduce(soma_local, op=MPI.SUM, root=0) # Reduz a soma local para o processo raiz

if rank == 0:
    print("Resultado: ", soma_global) # Exibe o resultado final no processo raiz
