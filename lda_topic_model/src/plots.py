import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_plot_stats(path):
    data = pd.read_csv(path)
    ret = []
    for s in data["vocab_size"]:
        ret.append(s)

    x = []
    y = []
    for i in range(9, len(ret), len(ret)//20):
        x.append(i)
        y.append(ret[i])
    return x, y

def add_labels(ax, x, y):
    labels = [ str(a*100//170)+ "%" for a in x]
    
    ax.set_ylabel("Vocabulary size")
    ax.set_xlabel("N %")
    ax.set_title("Frequency restriction in vocabulary")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.8, box.height*1.8])
    for i, v in enumerate(y):
        ax.text(x[i], v+10, "%d" %v, ha="center")

def generate_plot(path):
    x, y = get_plot_stats(path)
    fig, ax = plt.subplots()
    width = 0.35  # t, he width of the bars
    ax.plot(x, y, 'o')
    add_labels(ax, x, y)
    plt.ylim([0, y[0] + 30])