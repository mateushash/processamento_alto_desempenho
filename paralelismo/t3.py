from mpi4py import MPI 
import numpy as np 

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()0 
    if rank == 0: 
        numData = 10 
        comm.send(numData, dest=1) 
        data = np.linespace(0.0. 2.12, numData) 
        comm.Send(data, dest=1) 
    elif rankd ==1: 
        numdata = com.receIsource =0 ) 
        data = np.empty(numData, dtype = 'd') 
        comm.Recv(data,)
