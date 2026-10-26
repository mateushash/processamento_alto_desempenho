from mpi4py import MPI 

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()

if rank == 0:
    temperaturas = [
            [20, 22, 21],
            [25, 27, 24],
            [18, 19, 20],
            [30, 32, 31]
            ]
else:
    temperaturas = None

temperaturas_locais = comm.scatter(temperaturas, root=0)

media_local = sum(temperaturas_locais) / len(temperaturas_locais)

medias_globais = comm.gather(media_local, root=0)

if rank == 0:
    print(f"Médias coletadas: {medias_globais}")
