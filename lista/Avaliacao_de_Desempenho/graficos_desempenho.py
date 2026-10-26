import matplotlib.pyplot as plt
import numpy as np

def speed_up_graph(speed_up_x=[[]], speed_up_y=[[]], title=[['Speed Up']]):
# Plot the perfect linear scaling reference line
    speed_up_x_perfect = np.linspace(1, max(speed_up_x[0]), 100)
    speed_up_y_perfect = speed_up_x_perfect

    plt.plot(speed_up_x_perfect, speed_up_y_perfect, label='Speed Up Perfeito', color='blue', linestyle='--', linewidth=2)

# Plot actual measured results (dots connected by a curve/line)
# 1 Primos
    plt.plot(speed_up_x[0], speed_up_y[0], label="Speed Up Real Primos", color='red', marker='o', markersize=8, linewidth=2)

# 2 Monte Carlo
    plt.plot(speed_up_x[0], speed_up_y[1], label="Speed Up Real Monte Carlo", color='green', marker='o', markersize=8, linewidth=2)

    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Speed Up', fontsize=12)
    plt.title("Speed Up", fontsize=14)
# Set equal limits so the perfect line looks like a true 45-degree angle
    plt.xlim(1, max(speed_up_x[0]))
    plt.ylim(1, max(speed_up_y[0]) + 1)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    plt.show()

def efficiency_graph(efficiency_x=[[]], efficiency_y=[[]], title=[['Efficiency']]):
# 1 Primos
    plt.plot(efficiency_x[0], efficiency_y[0], color='red', marker='o', markersize=8, linewidth=2)

# 2 Monte Carlo
    plt.plot(efficiency_x[0], efficiency_y[1], color='blue', marker='o', markersize=8, linewidth=2)

    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Eficiencia', fontsize=12)
    plt.title("Eficiencia", fontsize=14)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    plt.show()


###################### DATA
speed_up_x = [[1, 2, 4, 6]] 
speed_up_y = [[
        1,
        1.01097413024019,
        2.24724296909358,
        2.26297826895638
    ],
    [ 
        1,
        1.74912322862057,
        3.7216775102189,
        5.33258649476646
    ]]

efficiency_y = [[
        1,
        0.505487065120094,
        0.561810742273394,
        0.377163044826064,
    ],
    [
        1,
        0.874561614310285,
        0.930419377554724,
        0.88876441579441,    
    ]]

speed_up_graph(speed_up_x, speed_up_y)
efficiency_graph(speed_up_x, efficiency_y)
