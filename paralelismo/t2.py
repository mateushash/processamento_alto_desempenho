from mpi4py import MPI 

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    data = {"a": 7, "b": 3.14}
    for i in range(1, size):
        comm.send(data, dest=i)
    print(f"Data send: {data}")
else: 
    data = comm.recv(source=0)
    print(f"Process {rank} received data: {data}")
