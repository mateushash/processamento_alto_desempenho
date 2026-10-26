from mpi4py import MPI

comm = MPI.COMM_WORLD 
rank = comm.Get_rank() 

valor = rank * 15 + 3 
print(f"Rank {rank} - Valor Local: {valor}")

maior = comm.reduce(valor, op=MPI.MAX, root=0)

if rank == 0:
    print(f"Maior Valor: {maior}")
