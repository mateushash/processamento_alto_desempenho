import numpy as np

def matrix_mutlt(A, B, N, BS):
    C = np.zeros((N, N), dtype=A.dtype)
    for ii in range(0, N, BS):
        for jj in range(0, N, BS):
            for kk in range(0, N, BS):
                for i in range(ii, min(ii + BS, N)):
                    for j in range(jj, min(jj + BS, N)):
                        for k in range(kk, min(kk + BS, N)):
                            C[i, j] += A[i, k] * B[k, j]
