import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def add_labels(ax, rects1, x, dd):

    labels = ["1", "2", "3", "4", "5"]

    labels = [k.replace("_", " ") for k, v in dd.items()]

    ax.set_ylabel("Quantità")
    ax.set_xlabel("N° statistica")
    ax.set_title("Statistiche popolazione")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation='vertical')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.5, box.height*1.5])
    
    autolabel(rects1, ax)


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def generate_plot(path):
    with open(path) as f:
        dd = eval(f.read())
    dd.pop('total')
    
    stp = [v for k, v in dd.items()]

    x = np.arange(len(dd))  # the label locations

    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars
    rects1 = ax.bar(x, stp, width)

    add_labels(ax, rects1, x, dd)
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))