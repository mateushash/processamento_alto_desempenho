from mpi4py import MPI 
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    N = 10
    A = np.random.random((N, N))
    x = np.random.random(N)
    n_rows = N//size
    n_cols = N
    matrix_A_array = np.empty((0, n_rows, n_cols))

    for i in range(0, size):
        # Slice A from rank*n_rows to the next n_rows number of rows(rank*n_rows+n_rows)
        sub_matrix = A[i * n_rows: i * n_rows + n_rows]
        # reshape the sub_matrix to (1, n_rows, n_cols)
        sub_matrix = np.expand_dims(sub_matrix, axis=0)
        # Append the sub_matrix to the matrix_A_array
        matrix_A_array = np.append(matrix_A_array, sub_matrix, axis=0)

        if i == size - 1:
            last_matrix = A[size * (N//size):]
            zeros_rows = np.zeros((n_rows - N%size, n_cols))
            last_matrix = np.vstack([last_matrix, zeros_rows])
            matrix_A_array = np.append(matrix_A_array, np.expand_dims(last_matrix, axis=0), axis=0)
else:
    N = None
    A = None
    x = None

N = comm.bcast(N, root=0)

if N is None:
    raise ValueError("N is not defined on rank 0")
elif N == 0:
    raise ValueError("N must be greater than 0")

local_A = comm.scatter(matrix_A_array, root=0)
print(f"Matrix A on rank {rank}:\n{local_A}")
