from mpi4py import MPI

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()

blocos = True

if (rank == 0 and blocos):
    dados = [
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [10,11,12]
            ]
elif rank == 0:
    # se usar -n 4, a lista de dados deve ter 4 elementos, um para cada processo
    dados = [10, 20, 30, 40]
else:
    dados = None 


#valor = comm.scatter(dados, root=0)
#print(f"Processo {rank} recebeu o valor: {valor}")

bloco = comm.scatter(dados, root=0)
soma_local = sum(bloco) 

print(f"Processo {rank} recebeu o bloco: {bloco} e a soma local é: {soma_local}")

