import sys

import numpy as np

import benchmarks as bch
from stencil2D import stencil2D as ste

if __name__ == "__main__":
    print("Choose a version Please: ")
    print("0 - V0: Referencia")
    print("1 - V1: MUL inves de DIV")
    print("2 - V2: Vetorizaçao em Numpy")
    print("quit - Exit")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else: 
        choice = input()
    match choice:
        case '0':
            bch.write_benchmark_metrics([ste.stencil2D_V0], experiment_title="V0")
            print("V0 results saved to V0results.csv")
        case '1':
            bch.write_benchmark_metrics([ste.stencil2D_V1], experiment_title="V1")
            print("V1 results saved to V1results.csv")
        case '2':
            bch.write_benchmark_metrics([ste.stencil2D_numpy], experiment_title="V2 - Numpy")
            print("V2 results saved to V2_numpy_results.csv")


        case 'quit' | 'exit' | 'quit()' | 'exit()' | 'q' | 'e':
            print("Exiting...")
            sys.exit()
        case _:
            print("Invalid option")
