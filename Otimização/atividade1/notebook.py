# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: Conda ai_env
#     language: python
#     name: ai_env
# ---

# %% [markdown]
# # Parte I – Análise conceitual
#
# # Questão 1 – Otimização não significa apenas “fazer menos contas”
#
# Supondo que A e B rodam no mesmo computador. O programa B pode ter uma melhor localidade espacial que o A, como é o exemplo de casos de acesso de matrizes por colunas(pior localidade) e por linhas(melhor localidade), nesse caso talves os acessos realizados por A, mesmo que menores, tem uma localidade pior.
#
# O programa A talves esteja carregando na cache dados, mas apenas usando um desses dados em cada operacao, precisando entao carregar novos dados para entao realizar suas outras operações.
#
# A estrutura de dados de A pode ser menos otimizada que a de B,como nos casos em que fazer busca de acessos em uma lista gera um custo maior do que fazer em um set.
#
# O programa A pode estar gerando um overhead ao chamar funções que o programa B nao chama
#
# # FALTA EXEMPLO
#
# # Questão 2 – Hierarquia de memória
# a) Porque o acesso a RAM é mais demorado que o acesso aos caches Ls, que por sua vez são mais demorados que os acessos aos registradores.
#
# b) Um cache miss ocorre quando o dado buscado nao esta no nivel acessado, forçando a CPU a buscar o dado em um nivel abaixo. Eg: buscar em L3 um dado que esta na RAM
#
# c) Um cache hit ocorre quando o dado buscado esta no nivel consultado
#
# d) Localidade Espacial: Os vizinhos dos dados acessados tem a chance de serem acessados.
#
# Localidade Temporal: Os dados agora acessados tem a chance de serem acessados novamente em breve
#
# e) O primeiro padrao de acesso faz uso sequencial, oq gera uma localidade espacial melhor, pois os dados estao carregados em sequencia e tabem uma localidade temporal melhor, pois como o acesso esta ocorrendo sequencialmente, o proximo dado sera acessado em seguida.
# O segundo padrao tem um stride muito grande e por isso a memoria cache precisa ser constantemente atualizada, levando a muito mais cache miss


# %% [markdown]
# # Parte II – Otimização sequencial
# # Questão 3 – Análise do código
# resultado = []
# inves de declarar uma lista vazia, fazer a alocação previa do espaço de memoria 
#
# resultado.append(valor)
# previsa realocar toda a memoria anterior mais o espaço para o append em cada execução, como o tamanho e o tipo de dado sao conhecidos, fazer a alocação previa é melhor
#
# fazer 2*math.sqrt(x[i]) para diminuir o overhead


# %%
import math 
import numpy as np
from numba import njit


# %%
# Versao A 
@njit
def calcula_A(x):
    resultado = []

    for i in range(len(x)):
        valor = math.sqrt(x[i]) + math.sqrt(x[i])
        resultado.append(valor)

    return resultado

# %%
# Versao B 
@njit
def calcula_B(x):
    resultado = [0.0] * len(x)
    size = len(x)

    for i in range(size):
        valor = 2 * math.sqrt(x[i])
        resultado[i] = valor

    return resultado

# %%
# Versao C
@njit
def calcula_C(x):
    size = len(x)
    resultado = np.empty(size, dtype=np.float64)

    for i in range(size):
        valor = 2 * math.sqrt(x[i])
        resultado[i] = valor

    return resultado

# %%
from time import perf_counter
element_size = (10_000, 100_000, 1_000_000, 10_000_000)

def time_benchmark(f, *args):
    resultados = []
    execution_times = []
    for i in range(5):
        t0 = perf_counter()
        resultado = f(*args)
        execution_times.append(perf_counter() - t0)
        resultados.append(resultado)
    return resultados, execution_times

def metrics(execution_times):
    median = np.median(execution_times)
    max = np.max(execution_times)
    min = np.min(execution_times)
    mean = np.mean(execution_times)
    return median, max, min, mean


# %%
import csv

headers = ['f_name', 'size', 'median', 'max', 'min', 'mean']
data = []
resultados = []

for size in element_size:
    for f in (calcula_A, calcula_B, calcula_C):
        resultado, execution_times = time_benchmark(f, np.arange(size))
        md, mx, mn, avg = metrics(execution_times)
        
        data.append([f.__name__, size, md, mx, mn, avg])
        resultados.append(resultado)

with open('resultados.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(data)

# %%
import pandas as pd 
df = pd.read_csv('resultados.csv')
print(df)

# %%
reshaped = (
    df.pivot(index="size", columns="f_name", values="mean")
      .rename(columns={
          "calcula_A": "mean_A",
          "calcula_B": "mean_B",
          "calcula_C": "mean_C",
      })
      .reset_index()
)

print(reshaped)


# %%
speed_df = pd.DataFrame({
    'speedA': reshaped['mean_A'] / reshaped['mean_A'],
    'speedB': reshaped['mean_A'] / reshaped['mean_B'],
    'speedC': reshaped['mean_A'] / reshaped['mean_C'],
})

speed_df.insert(0, 'size', reshaped['size'])
print(speed_df)

# %%
import matplotlib.pyplot as plt

# A is the baseline, so speedup = 1
#plt.axhline(y=1, linestyle="--", label="A", color='green')
plt.plot(speed_df["size"], speed_df["speedA"], marker="o", label="A")
plt.plot(speed_df["size"], speed_df["speedB"], marker="o", label="B")
plt.plot(speed_df["size"], speed_df["speedC"], marker="o", label="C")

plt.xscale("log")

plt.xlabel("Input size")
plt.ylabel("Speedup over implementation A")
plt.title("Speedup vs. Input Size")

plt.legend()
plt.grid(True, alpha=0.3)

plt.show()


# %% [markdown]
# # Questao 5 - Speedup
#
# a) A versao C (implementada em numpy) 
# b) Somente para a versao B
# c) Para C com base no aumento do numero de dados espera-se que exista uma demora maior de processamento quando os dados aumento na ordem de 10x a quantidade anterior o que explica o declinio visto no grafico entre 10e6 e 10e7. Agora o speed up tem um salto entre 10e4 e 105
# d) a versao numpy utiliza uma estrutura de dados diferente, o que sobrescreve a maneira que operadores padrões funcionam, como o caso do [] de acesso, logo apesar do código ser semelhante visualmente, sua estrutura de funcionamento é diferente logicamente.
#

# %% [markdown]
# # Parte III – Cache e organização da memória


# %%
# Algoritmo 1 - percurso por linhas linhas
@njit
def sum_A(A, N):
    soma = 0.0
    for i in range(N):
        for j in range(N):
            soma += A[i, j]

# Algoritmo 2 - percurso por colunas
@njit
def sum_B(A, N):
    soma = 0.0
    for j in range(N):
        for i in range(N):
            soma += A[i, j]

# %% [markdown]
# # Q6 - Previsão antes do experimento 
#
# o algoritmo 2 por conta da localidade espacial, onde os elementos sao carregados sequencialmente nas caches, ou seja, as linhas sao carregadas contiguamente na memoria entao o vizinho do elemento atual provavelmente ja esta carregado na memoria, enquanto q na implementacao A ha um risco maior de cache miss

# %%
N = (500, 1000, 2000, 3000, 4000)

headers = ['f_name', 'size', 'median', 'max', 'min', 'mean']
data = []
resultados = []

for size in N:
    A = np.random.random((size, size))
    for f in (sum_A, sum_B):
        resultado, execution_times = time_benchmark(f, A, size)
        md, mx, mn, avg = metrics(execution_times)
        
        data.append([f.__name__, size, md, mx, mn, avg])
        resultados.append(resultado)

with open('resultados_matrix.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(data)

# %%
df = pd.read_csv('resultados_matrix.csv')
print(df)

# %%
reshaped = (
    df.pivot(index="size", columns="f_name", values="mean")
      .rename(columns={
          "sum_A": "mean_A",
          "sum_B": "mean_B",
      })
      .reset_index()
)

print(reshaped)


# %%
speed_df = pd.DataFrame({
    'speedA': reshaped['mean_A'] / reshaped['mean_A'],
    'speedB': reshaped['mean_A'] / reshaped['mean_B'],
})

speed_df.insert(0, 'size', reshaped['size'])
print(speed_df)

# %%
plt.plot(reshaped["size"], reshaped["mean_A"], marker="o", label="A")
plt.plot(reshaped["size"], reshaped["mean_B"], marker="o", label="B")

plt.xlabel("Input size")
plt.ylabel("Execution Time")
plt.title("Execution Time Means for A and B Matrix algo")

plt.legend()
plt.grid(True, alpha=0.3)

plt.show()


# %%
plt.plot(speed_df["size"], speed_df["speedA"], marker="o", label="A")
plt.plot(speed_df["size"], speed_df["speedB"], marker="o", label="B")

plt.xlabel("Input size")
plt.ylabel("Speedup over implementation A")
plt.title("Speedup vs. Input Size for Matrix")

plt.legend()
plt.grid(True, alpha=0.3)

plt.show()

# %%
# Calculo de R = T_colunas/T_linhas
reshaped['R'] = reshaped['mean_B'] / reshaped['mean_A']
plt.plot(reshaped["size"], reshaped["R"], marker="o", label="R")

plt.xlabel("Input size")
plt.ylabel("R value")
plt.title("R computing")

plt.legend()
plt.grid(True, alpha=0.3)

plt.show()



# %% [markdown]
# # Questão 7 – Experimento
# R é uma constante de proporção entre o tempo de execucao de sum_A(linhas) e sum_B(colunas) e ele representa para um dado N o quanto que T_colunas muda em relação proporcional a T_linhas, pois pela eq: 
#
#   T_colunas = R T_linhas
#
# ve-se que T_colunas é proporcional a T_linhas por R. dado um T_colunsa fixo e R:
#
#  se 0<R<1, sabe-se que o valor de T_linhas é necessariamente maior que T_linhas, pois um Numero N multiplicado por um valor entre 0 e 1 eh menor que o proprio N
#
# Se R>1, sabe-se que o valor T_linhas é menor que T_colunas, pois um Numero N multiplicado por um valor maior que 1 eh maior que o proprio N
#
# Se R=1, sabe-se que o valor T_linhas é igual a T_colunas, pois um Numero N multiplicado por um valor igual a 1 eh igual ao proprio N
#
# Note que R no experimento é sempre menor que 1, oq contrario ao esperado indica que a execução por colunas é mais rapida que a execução por linhas
#
#
#
#
#

# %% [markdown]
# # Questão 12

# %%
def plot_quadratic(a, b, c, x_max=10, ax=None, label=None, **kwargs):
    """Plot y = ax² + bx + c for x in [0, x_max]."""
    if ax is None:
        ax = plt.gca()
    x = np.linspace(0, x_max, 400)          # <-- starts at 0, so only positive x
    y = a * x**2 + b * x + c
    ax.plot(x, y, label=label or f"y = {a}x² + {b}x + {c}", **kwargs)
    return ax


fig, ax = plt.subplots(figsize=(8, 6))

plot_quadratic( 2,   0.0,  0.0, x_max=8, ax=ax, color="C2", label="y = 2x²")
plot_quadratic( 1.0, 0.0,  0.0, x_max=8, ax=ax, color="C0", label="y = x²")
plot_quadratic( 0.5, 0.0,  0.0, x_max=8, ax=ax, color="C1", label="y = 0.5x²")

# Axes through the origin
ax.axhline(0, color="black", lw=0.8)
ax.axvline(0, color="black", lw=0.8)

ax.set_xlim(left=0)          # hard-lock the visible region to x ≥ 0
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Quadratic curves — positive x-axis only")
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# O(N²) indinca uma equçao polinomial de segundo grau do tipo: 
#
# y = ax² + bx + c
#
# Como observado no grafico acima, apesar dos polinomios terem o mesmo grau, a maneira como eles 'abrem' varia drasticamente o valor a. Por essa razao um algoritmo de ordem 2 com 0<a<1 como o caso das linha amarela tem um crescimento temporal muito menor que algoritmos de ordem 2 com a > 1 caso da linha verde.
# isso considerando que o tempo de execução apenas depende do numero N de valores(no caso x), mas na verdade esse tempo tambem depende do acesso a memoria cache, que pode ser afetado por cache miss ou cache hit. Quando um cache miss ocorre devido por ex, a um stride muito longo, é necessário buscar em niveis inferiores de memoria o dado necessário para a proxima computação, agregando no tempo de execução.
# Há também Questões de otimização envolvidas na linguagem escolhida, que dependendo da sua estrutura de dados pode afetar ainda mais a maneira como a memoria precisa ser alocada, acessada e liberada. Em resumo, quanto mais otimizado a implementacao do problema, considerando as ferramentas disponiveis na linguagem(como alocação previa) e a estrutura de dados do problemas(por exemplo listas e sets) menor sera o tempo execução agregado a proporcionalidade dos dados. Conclui-se que o tempo de execução do programa não soh depende do numero de dados, mas tambem como a sua implementação(linguagem + estrutura de dados) foi feita.

# %% [markdown]
## Parte VIII – Investigação livre
## Questão 13 – A máquina também faz parte do experimento
#
# Processador: amd radeon ryzen 5 8600g
#
# nucleos: 6
#
# RAM: 16gb
#
# cache L1: 0 
#
# cache L2: 6 MB
#
# cache L3: 16 MB
