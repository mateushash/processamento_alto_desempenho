# PARTE II - PROFILING
## Questão 2 — Identificação de gargalos
### a) A função que consome mais tempo de execução segundo o profiler é a stencil2D_V0 com 99.29% do tempo total(tottime)
### b) A expectativa inicial era de que quanto maior a quantidade de elementos no vetor, maior o tempo de execução, o que se observa na média dos tempos de execução(ver restultados V0.csv). O profiller apenas mostra por quanto tempo a função v0 foi executada.
### c) O profilling permite identificar onde os gargalos se encontram na execução do programa. Em casos de programas complexos com varais chamadas de funções, o profiler permite que o usuario indentfique qual delas esta comprometendo o desempenho do programa.

# Parte III — Complexidade computacional
## Questão 3 — Escalabilidade teórica
### Pela figura V0_data_vs_interpolation.png é possível observar que a complexidade assintótica é O(n^2). Pelo gráfico ao se dobrar a quantidade de elementos, o tempo crsce praticamente quadraticamente. O algoritmo stencil2D_V0 possui dois loops com range(1, N-1) intrelaçados, logo se espera que a execução se de pela formula:
### ((N-1) - 1) * ((N-1) - 1) = (N-2)^2 = O(N^2)
### O grafico V0_data_vs_interpolation.png mostra que a complexidade é O(n^2)

# Parte IV — Intensidade computacional
## Questão 4 — Operações versus bytes 
### 

# Parte V — Eliminação de operações
## Questão 5 — Divisão versus multiplicação
### Existe um ganho mensuravel como o visto pelo grafico V0_vs_V1 mas em favor do algrotimo V0(divisao) mas ele é desprezivel. Microotimizações aritmeticas podem ter impacto em um algoritmo dominado por memorio por conta da maneira como essas operações são realizadas pelos registradores na CPU, instruções de divisao (DIV) sao geralmente mais lentas que as de multiplicacao (MUL). Como python puro não compila o programa antes, as operações de DIV nao sao otimizadas, como no caso de C/C++, por isso era de se esperar que a versao V1 fosse mais rapida que V0, mas não foi o caso observado.

# Parte VI — Vetorização
## Questão 6 — NumPy

1. Elimination of Python Loop Overhead

In your first version (stencil2D_V1), Python has to evaluate the loop conditions and interpret each line of code inside the nested loops \((N-2) \times (N-2)\) times.
If \(N = 1000\), that is roughly 1,000,000 iterations.
* In Python, every single loop iteration incurs heavy interpretative overhead (checking object types, resolving dynamic references, and wrapping/unwrapping numbers).
* In the NumPy version, the loop happens entirely at the compiled C-extension level, which runs at native hardware speeds.

2. Slicing Creates Views, Not Copies

NumPy's slicing notation (like A[:-2, 1:-1]) does not actually copy any data in memory. Instead, it creates a "view".
A view is simply a small pointer object that tells NumPy to look at the same block of memory but with a shifted starting index and boundaries. This means setting up the matrices for the calculation takes practically zero time.

3. Pointer Chaining vs. Contiguous Memory Access

Look at how data is accessed in both versions:
* B\[i\][j] (Bad): This forces Python to look up the row pointer B\[i\] first, create a temporary reference to that subarray object, and then perform a second lookup for index [j]. Doing this millions of times causes immense pointer-chasing overhead.
* Vector Slices (Good): NumPy array operations read entire blocks of numbers that sit right next to each other in your computer's RAM (contiguous memory). This allows the CPU to fetch data efficiently, maximizing CPU Cache hits.

4. SIMD (Single Instruction, Multiple Data) Vectorization

Because the NumPy version describes the operation as a whole-array math problem, compiled C libraries (or BLAS backends) can leverage SIMD hardware instructions (like AVX or SSE) on your CPU.
Instead of adding one pixel neighborhood at a time, the processor can load 4, 8, or 16 floating-point values into specialized registers and add them all together in a single clock cycle.

# Parte VII — Uso de memória
## Questão 7 — Estimativa de memória
A partir de 4000 elementos já se tem 244mb para armazenar as duas matrizes, oq na maioria dos cpus de desktop de consumidores não oferece(96-128mb), fazendo-se então necessário o uso da RAM. Processadores especializados como o AMD EPYC X-Series tem um cache L3 de 1gb, oq permitiria esses processadores a usar pouco mais de 8000 elementos(976mb) na memoria cache.

# Parte VIII — Layout de memória
## Questão 8 — C-order e F-order
The core difference between order="C" and order="F" is how the matrix elements are arranged and stored in your computer's sequential memory lines.
While both commands produce a matrix that looks identical when printed, they structure the underlying memory address space differently, which drastically changes execution speed depending on how you iterate over or modify the data later.

The Breakdown

• order="C" (C-contiguous / Row-Major): This is the default in NumPy. Elements within the same row are stored next to each other in memory. Row 0 is stored completely, followed immediately by Row 1, Row 2, and so on.
• order="F" (Fortran-contiguous / Column-Major): Elements within the same column are stored next to each other in memory. Column 0 is stored completely, followed immediately by Column 1, Column 2, and so on.

Visualizing the Memory Layout

Imagine an \(N \times N\) matrix where \(N=2\):
\(\left[\begin{matrix}1&2\\ 3&4\end{matrix}\right]\)
Behind the scenes, your computer's RAM is completely flat. Here is how that 2D matrix is unrolled into a 1D linear array in memory:
• order="C" Layout: [ 1, 2, 3, 4 ] (Row 0 elements first, then Row 1 elements)
• order="F" Layout: [ 1, 3, 2, 4 ] (Column 0 elements first, then Column 1 elements)

Why Does This Matter? (The Performance Impact)

Modern CPUs do not pull data from RAM one single number at a time. Instead, they fetch chunked blocks of memory called cache lines into ultra-fast L1/L2/L3 caches.
If your code reads memory sequentially as it is physically arranged, it triggers a fast cache hit. If your code jumps across memory blocks, it triggers a slow cache miss, forcing the CPU to fetch from RAM again.
• If you are processing data Row-by-Row: Use order="C". (e.g., summing across axis 1, looping over rows).
• If you are processing data Column-by-Column: Use order="F". (e.g., summing across axis 0, looping over columns).
• Interoperability: Certain external mathematical libraries written in Fortran or C++ (like standard BLAS/LAPACK routines for heavy linear algebra computations) strictly expect order="F" and will perform a costly internal copy operation if you pass them a "C" matrix.

# Parte IX — Stride
## Questão 9 — Custo por acesso

# Parte X — Blocking / Tiling
## Questão 10 — Multiplicação matricial em blocos

