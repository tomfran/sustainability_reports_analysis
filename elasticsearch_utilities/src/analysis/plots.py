import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm

def get_verbose_density_plot(stats_path, label, filename):
    
    stp = []
    with open(stats_path) as f:
        stp = eval(f.read())
    sns.set()
    fig, ax = plt.subplots(figsize = (10,7))
    ax = sns.distplot(stp, kde=True, hist = True, norm_hist = False, label = label)
    # ax.set_xticks(np.arange(0,1.1,0.1))
    ax.set(xlabel="Valore", ylabel = "N° sample")
    ax.legend()
    ax.set(xlim=(0))  
    # ax = sns.distplot(pos)
    # plt.show()
    plt.savefig(f"elasticsearch_utilities/stats/plots/{filename}.png")