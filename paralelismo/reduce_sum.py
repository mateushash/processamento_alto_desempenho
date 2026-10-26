from mpi4py import MPI

comm = MPI.COMM_WORLD 
rank = comm.Get_rank() 

valor_local = (rank + 1) * 10 

soma = comm.reduce(valor_local, op=MPI.SUM, root=0)

if rank == 0:
    print(f"Soma Globbal: {soma}")
