from mpi4py import MPI 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    numero = 100
else:
    numero = None


numero = comm.bcast(numero, root=0)

print(f"Process {rank} received the number: {numero}")

def func1(comm):
    if rank == 0:
        parametros = {
                "N": 10000,
                "inicio": 0,
                "fim": 100, 
                "metodo": "Monte Carlo"
                }
    else:
        parametros = None
    
    parametros = comm.bcast(parametros, root=0)

    print(f"Process {rank} received the parameters: {parametros}")


func1(comm)

