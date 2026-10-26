import numpy as np


def stencil2D_V0(A):
    N = A.shape[0]
    B = np.zeros_like(A)
    for i in range(1, N-1):
        for j in range(1, N-1): 
            B[i][j] = (A[i-1][j] + A[i+1][j] + A[i][j-1] + A[i][j+1] + A[i][j]) / 5.0
    return B

def stencil2D_V1(A):
    N = A.shape[0]
    B = np.zeros_like(A)
    for i in range(1, N-1):
        for j in range(1, N-1): 
            B[i][j] = (A[i-1][j] + A[i+1][j] + A[i][j-1] + A[i][j+1] + A[i][j]) * 0.2 
    return B
    
def stencil2D_numpy(A):
    B = np.zeros_like(A)
    B[1:-1, 1:-1] = (
        A[:-2, 1:-1]
        + A[2:, 1:-1]
        + A[1:-1, :-2]
        + A[1:-1, 2:]
        + A[1:-1, 1:-1]
    ) * 0.2

    return B
