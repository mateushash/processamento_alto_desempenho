import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import data

def speed_up_graph(speed_up_x=[], speed_up_y=[], title='Speed Up', color='red'):
# Plot the perfect linear scaling reference line
    speed_up_x_perfect = np.linspace(1, max(speed_up_x), 100)
    speed_up_y_perfect = speed_up_x_perfect

    plt.plot(speed_up_x_perfect, speed_up_y_perfect, label='Speed Up Perfeito', color='green', linestyle='--', linewidth=2)
# Plot actual measured results (dots connected by a curve/line)
    plt.plot(speed_up_x, speed_up_y, label=f"Speed Up {title}", color=color, marker='o', markersize=8, linewidth=2)


    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Speed Up', fontsize=12)
    plt.title("Comparação de Speed Up em função de N", fontsize=14)
# Set equal limits so the perfect line looks like a true 45-degree angle
    plt.xlim(1, max(speed_up_x))
    plt.ylim(1, max(speed_up_y) + 1)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    #plt.savefig(f'{title}.png', dpi=300, bbox_inches='tight')
    #plt.show()

def efficiency_graph(speed_up_x=[], speed_up_y=[], title='Efficiency', color='red'):
    plt.plot(speed_up_x, speed_up_y, label=f"Efficiency {title}", color=color, marker='o', markersize=8, linewidth=2)


    plt.xlabel('Número de Processos', fontsize=12)
    plt.ylabel('Eficiencia', fontsize=12)
    plt.title("Comparação de Eficiencia em relação a N", fontsize=14)

    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)

    #plt.savefig(f'{title}.png', dpi=300, bbox_inches='tight')
    #plt.show()


###################### DATA
dataframe = pd.read_csv("resultados.csv")

dataframe = dataframe[[
    'N',
    'p',
    'S(p)',
    'E(p)'
    ]]

speed_up_x = dataframe["p"].iloc[0:4]
colors = ['red', 'blue', 'orange', 'purple', 'brown']

for i in range(5):
    speed_up_y = []

    speed_up_y = dataframe["S(p)"].iloc[i*4:i*4+4]

    speed_up_graph(speed_up_x, speed_up_y, title=f'N = {dataframe["N"][i*4]}', color=colors[i])

plt.show()

for i in range(5):
    efficiency_y = []

    efficiency_y = dataframe["E(p)"].iloc[i*4:i*4+4]

    efficiency_graph(speed_up_x, efficiency_y, title=f'Efficiency - {dataframe["N"][i*4]}', color=colors[i])

plt.show()
