from mpi4py import MPI

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()

resultado_local = rank * 10 

resultados = comm.gather(resultado_local, root=0)


if rank == 0:
    print(f"Resultados coletados no processo {rank}: {resultados}")

