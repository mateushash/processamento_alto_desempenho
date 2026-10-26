from mpi4py import MPI 
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = None
A = None
x = None
n_rows = None 
n_cols = None
matrix_A_array = None

if rank == 0:
    N = 8000
    A = np.random.randint(0, N, (N, N))
    x = np.random.randint(0, N, (N,))
    n_rows = N//size
    n_cols = N
    matrix_A_array = []

    # create submatrices of A in the shape of (N, N//size) and store the last rows in case N%size is not zero into a separate matrix
    for i in range(0, size):
        # Slice A from rank*n_rows to the next n_rows number of rows(rank*n_rows+n_rows)
        sub_matrix = A[i * n_rows: i * n_rows + n_rows]
        # reshape the sub_matrix to (1, n_rows, n_cols)
        #sub_matrix = np.expand_dims(sub_matrix, axis=0)
        # Append the sub_matrix to the matrix_A_array
        matrix_A_array.append(sub_matrix)

    # the last matrix has the remaining rows if N%size is not zero, 
    if N % size != 0:
        last_matrix = A[(size) * n_rows:]
        # iterate over the remaining rows and append them to the first matrix in the matrix_A_array
        for i, row in enumerate(last_matrix):
            # expand one dimension so the row is now a matrix of shape (1, n_cols) and append it to the first matrix in the matrix_A_array
            row = np.expand_dims(row, axis=0)
            matrix_A_array[i] = np.vstack([matrix_A_array[i], row])

        last_matrix = np.expand_dims(last_matrix, axis=0)

N = comm.bcast(N, root=0)
if N is None:
    raise ValueError("N is not defined on rank 0")
elif N == 0:
    raise ValueError("N must be greater than 0")

local_A = comm.scatter(matrix_A_array, root=0)
#print(f"Matrix A on rank {rank}:\n{local_A}")
if local_A is None:
    raise ValueError(f"local_A is None on rank {rank}")

x = comm.bcast(x, root=0)

# test if both local_A as much colums as x has elements
if len(x) != local_A.shape[1]:
    raise ValueError(f"Vector x length {len(x)} does not match number of columns in local_A {local_A.shape[1]} on rank {rank}") 

local_y = np.matmul(local_A, x)
global_y = comm.gather(local_y, root=0)

if rank == 0:
# VALIDACAO
    # print(f"Global y before rearranging:\n{global_y}")

    if N % size != 0:
        # in this case the firs matrices got add an extra row from the last matrix, so we need to iterate over the global_y and remove the last element of the firsts N%size elements of the global_y
        last_elements = []
        for i in range(N % size):
            last_elements.append(global_y[i][-1])
            # remove the last element of the first local_y
            global_y[i] = global_y[i][:-1]

    # flatten the global_y list of arrays into a single array
    global_y = np.concatenate(global_y)
    global_y = np.append(global_y, last_elements)

    numpy_y = np.matmul(A, x)
    print(f"Result vector y:\n{global_y}")
    print(f"Validation    y:\n{numpy_y}")

    print(f"both equivalent?: {np.allclose(global_y, numpy_y)}")


