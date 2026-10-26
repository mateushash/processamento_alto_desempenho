import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import benchmarks as bm

def plot_polynomial(x, y, poly, degree):
    x_smooth = np.linspace(min(x), max(x), 100)
    y_smooth = poly(x_smooth)

    plt.figure(figsize=(8,5))
    plt.scatter(x, y, color='green', zorder=5, label='Data Points')
    plt.plot(
        x_smooth,
        y_smooth,
        color="blue",
        linewidth=2,
        label=f"Polynomial Interpolation (Degree {degree})",
    )
    plt.title("Polynomial Interpolation of Discrete Sequence")
    plt.xlabel("n / x-axis")
    plt.ylabel("y-axis")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)


def plot_data(df, marker='o', color='green', label='', title=''):
    plt.plot(df['size'], df['mean'], marker=marker, color=color, label=label)

    plt.xlabel("Input size")
    plt.ylabel("Mean Execution Time")
    plt.title(title)
    
    plt.legend()
    plt.grid(True, alpha=0.3) 


def speed_up_graph(speed_up_x=[], speed_up_y=[], title='Speed Up', color='red'):
    plt.plot(speed_up_x, speed_up_y, label=f"Speed Up {title}", color=color, marker='o', markersize=8, linewidth=2)


    plt.xlabel('Element Size', fontsize=12)
    plt.ylabel('Speed Up', fontsize=12)
    plt.title("Speed Up Comparison for 2 Versions")

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)


def read_data(dir: str = "./results/", file: str = "resultadosV0.csv"):
    df = pd.read_csv(dir + file)
    return df

def fit_data_polynomial(df, degree):
    x = np.array(df['size'])
    y = np.array(df['mean'])

    
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)

    return polynomial


if __name__ == "__main__":
    results_V0 = read_data() 
    match int(input("Enter an options: ")):
        case 0:
            # try to fit a polynomial of degree 2
            polynomial = fit_data_polynomial(results_V0, 2)
            plot_polynomial(results_V0['size'], results_V0['mean'], polynomial, 2)
            plot_data(results_V0, label='Real Execution Time', title="Element size x Mean Execution Time")
            plt.savefig("./results/Q3_polynomial_interpolation.png")
            plt.show()
        case 1:
            results_V1 = read_data(file="resultadosV1.csv")
            plot_data(results_V0, label='V0 Execution Time')
            plot_data(results_V1, label='V1 Execution Time', color="blue", title="V0 Sum vs V1 Multiplication")
            plt.savefig("./results/V0_vs_V1.png")
            plt.show()
        case 2:
            results_V2 = read_data(file="resultadosV2 - Numpy.csv")
            results_V2['speed_up'] = bm.calc_speed_up(list(results_V0['mean']), list(results_V2['mean'])) 
            speed_up_graph(results_V0['size'], results_V2['speed_up'], title='V0 vs V2')
            plt.savefig("./results/V0_vs_V2_speed_up.png")
            plt.show()

        case _:
            print("Invalid option")
