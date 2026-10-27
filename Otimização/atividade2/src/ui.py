import sys 
import matplotlib.pyplot as plt
import benchmarks as bch
import analysis as anal
from stencil2D import stencil2D as ste

def show_benchmarks_options(choice: str | None = None):
    print("BENCHMARKS")
    print("Choose a version Please: ")
    print("0 - V0: Referencia")
    print("1 - V1: MUL inves de DIV")
    print("2 - V2: Vetorizaçao em Numpy")
    print("quit - Exit")

    if (choice == None):
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

def show_analyssis_options():
    results_V0 = anal.read_data() 
    match int(input("Enter an options: ")):
        case 0:
            # try to fit a polynomial of degree 2
            polynomial = anal.fit_data_polynomial(results_V0, 2)
            anal.plot_polynomial(results_V0['size'], results_V0['mean'], polynomial, 2)

            anal.plot_data(results_V0['size'], results_V0['mean'], label='Real Execution Time', title="Element size x Mean Execution Time", x_label="Input size", y_label="Mean Execution Time")
            plt.savefig("./results/Q3_polynomial_interpolation.png")
            plt.show()
        case 1:
            results_V1 = anal.read_data(file="resultadosV1.csv")
            anal.plot_data( results_V0['size'], results_V0['mean'], label='V0 Execution Time',  x_label="Input size", y_label="Mean Execution Time")
            anal.plot_data( results_V1['size'], results_V1['mean'], label='V1 Execution Time', color="blue", title="V0 Sum vs V1 Multiplication", x_label="Input size", y_label="Mean Execution Time")
            plt.savefig("./results/V0_vs_V1.png")
            plt.show()
        case 2:
            results_V2 = anal.read_data(file="resultadosV2 - Numpy.csv")
            results_V2['speed_up'] = bm.calc_speed_up(list(results_V0['mean']), list(results_V2['mean'])) 
            anal.speed_up_graph(results_V0['size'], results_V2['speed_up'], title='V0 vs V2')
            plt.savefig("./results/V0_vs_V2_speed_up.png")
            plt.show()

        case _:
            print("Invalid option")


