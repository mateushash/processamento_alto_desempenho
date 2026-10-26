import matplotlib.pyplot as plt
import numpy as np

def speed_up_graph(speed_up_x=[], speed_up_y=[], title='Speed Up'):
# Plot the perfect linear scaling reference line
    speed_up_x_perfect = np.linspace(1, max(speed_up_x), 100)
    speed_up_y_perfect = speed_up_x_perfect

    plt.plot(speed_up_x_perfect, speed_up_y_perfect, label='Speed Up Perfeito', color='blue', linestyle='--', linewidth=2)
# Plot your actual measured results (dots connected by a curve/line)
    plt.plot(speed_up_x, speed_up_y, label='Speed Up Real', color='red', marker='o', markersize=8, linewidth=2)


    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Speed Up', fontsize=12)
    plt.title(title, fontsize=14)
# Set equal limits so the perfect line looks like a true 45-degree angle
    plt.xlim(1, max(speed_up_x))
    plt.ylim(1, max(speed_up_y) + 1)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    plt.show()

def efficiency_graph(speed_up_x=[], speed_up_y=[], title='Efficiency'):
    plt.plot(speed_up_x, speed_up_y, color='red', marker='o', markersize=8, linewidth=2)


    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Eficiencia', fontsize=12)
    plt.title(title, fontsize=14)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    plt.show()


###################### DATA
speed_up_x = [1, 2, 4, 6] 
primos_speed_up_y = [
        1,
        1.01097413024019,
        2.24724296909358,
        2.26297826895638
]
primos_efficiency_y = [
    1,
    0.505487065120094,
    0.561810742273394,
    0.377163044826064,
]

monte_carlo_speed_up_y = [
        1,
        1.74912322862057,
        3.7216775102189,
        5.33258649476646
]
monte_carlo_efficiency_y = [
    1,
    0.874561614310285,
    0.930419377554724,
    0.88876441579441,
]

speed_up_graph(speed_up_x, primos_speed_up_y, title='Speed Up - Primos')
efficiency_graph(speed_up_x, primos_efficiency_y, title='Efficiency - Primos')
speed_up_graph(speed_up_x, monte_carlo_speed_up_y, title='Speed Up - Monte Carlo')
efficiency_graph(speed_up_x, monte_carlo_efficiency_y, title='Efficiency - Monte Carlo')

