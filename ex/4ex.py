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
soma_local = np.sum(bloco) # Calcula a soma local do bloco
quantidade_local = len(bloco) # Calcula a quantidade local de elementos no bloco

soma_global = comm.reduce(soma_local, op=MPI.SUM, root=0) # Reduz a soma local para o processo raiz
quantidade_global = comm.reduce(quantidade_local, op=MPI.SUM, root=0) # Reduz a quantidade local para o processo raiz

if rank == 0:
    media_global = soma_global / quantidade_global # Calcula a média global
    print("Média Global: ", media_global) # Exibe a média global no processo raiz
    print("Média Global (usando numpy): ", np.mean(dados)) # Exibe a média global usando numpy para comparação
