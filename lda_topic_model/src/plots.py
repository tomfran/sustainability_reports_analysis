import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def get_plot_stats(path):
    data = pd.read_csv(path , sep=r'\s*,\s*', header=0, encoding='ascii', engine='python')
    x = data['N'].to_numpy()
    y = data['M'].to_numpy()
    z = data['size'].to_numpy()
    return x, y, z

def generate_plot(path, en="all"):
    plt.rcParams.update({'font.size': 10})
    x, y, z = get_plot_stats(path)
    fig = plt.figure(figsize=(9, 5), dpi=100, tight_layout=False)
    ax = Axes3D(fig)
    ax.set_title("Vocabulary size")
    ax.set_xlabel('N')
    ax.set_ylabel('M')
    if en == "top":
        ax.set_yticks([i for i in range(1,5)])
    ax.set_zlabel('size')
    surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.7)
    fig.colorbar(surf, shrink=0.4, aspect=5)
    ax.view_init(30, 55)
    plt.show()
