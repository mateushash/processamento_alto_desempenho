import time
import numpy as np

start = time.perf_counter()

N = 100000000
x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)

points = np.random.rand(N, 2) * 2 - 1 

circle = [point for point in points if point[0]**2 + point[1]**2 <= 1]

# for i in range(N):
#     for j in range(N): 
#         if x[i]**2 + y[j]**2 <= 1:
#             circle.append([x[i], y[j]])

pi = 4 * len(circle) / N

end = time.perf_counter()

print("Valor aproximado de pi:", pi)
print(f"Tempo de execução: {end - start:.4f} segundos")
