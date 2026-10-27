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


def plot_data(
        x, 
        y, 
        marker='o', 
        color='green', 
        x_label='',
        y_label='',
        label='', 
        title=''):
    plt.plot(x, y,  marker=marker, color=color, label=label)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
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



