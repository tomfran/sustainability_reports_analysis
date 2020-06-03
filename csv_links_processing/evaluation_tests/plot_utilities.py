import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


def get_plot_stats(path):

    websites = [[],[]] 
    websites_perc = [[],[]] 
    pdf_links = [[],[]] 
    pdf_links_perc = [[],[]] 
    depth = [[],[]] 
    home = [[],[]] 
    
    stats_list = [path+"/"+l for l in sorted(os.listdir(path))]
    for f in stats_list:
        with open(f, "r") as s:
            l = s.readlines()[1::]
            i = int("40" in f)
            websites[i].append(int(l[1].split(",")[-1]))
            websites_perc[i].append(round(float(l[2].split(",")[-1]), 2))
            pdf_links[i].append(int(l[4].split(",")[-1]))
            pdf_links_perc[i].append(round(float(l[5].split(",")[-1]), 2))
            depth[i].append(round(float(l[6].split(",")[-1]), 2))
            home[i].append(int(l[7].split(",")[-1]))

    stp = [websites]
    stp.append(websites_perc)
    stp.append(pdf_links)
    stp.append(pdf_links_perc)
    stp.append(depth)
    stp.append(home)

    return stp

def add_labels(ax, rects1, rects2, x, i):
    titles = ["Siti che hanno pubblicato", "Percentuale siti che hanno pubblicato", \
              "Numero di pdf utili", "Percentuale pdf utili", \
              "Profondità media", "Numero pdf in homepage"]
    ylab = ["Quantità", "Percentuale", \
            "Quantità", "Percentuale", \
            "Profondità", "Qauntità"]

    labels = ["1", "2", "3", "4", "5"]
    
    ax.set_ylabel(ylab[i])
    ax.set_xlabel("Valutazioni")
    ax.set_title(titles[i])
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.5, box.height*1.5])
    
    autolabel(rects1, ax)
    autolabel(rects2, ax)


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def generate_plot(stp):
    fig, ax = plt.subplots(3, 2,figsize=(16,18))
    fig.tight_layout(pad=18.0)
    ax = ax.flatten()
    for i in range(6):
        a = stp[i][0]
        b = stp[i][1]
        x = np.arange(len(a))  # the label locations
        width = 0.35  # the width of the bars
        rects1 = ax[i].bar(x - width/2, a, width, label='60 thold')
        rects2 = ax[i].bar(x + width/2, b, width, label='40 thold')
        add_labels(ax[i], rects1, rects2, x, i)
        if i == 1:
            ax[i].legend(loc='center left', bbox_to_anchor=(1, 0.5))


def get_density_depth():
    pos = []
    with open("misc/depths_positive.txt") as f:
        pos = [int(l.replace('\n', '')) for l in f.readlines()]
    neg = []
    with open("misc/depths_negative.txt") as f:
        neg = [int(l.replace('\n', '')) for l in f.readlines()]

    sns.set()
    bins=np.arange(min(pos), max(pos) +1)
    fig, ax = plt.subplots(figsize = (10,5))
    ax = sns.distplot(pos, bins = bins ,kde=True,hist_kws={"rwidth":1}, hist = True, norm_hist = False, label = "Bilanci di sostenibilità")
    bins=np.arange(min(neg), max(neg) +1)
    ax = sns.distplot(neg, bins = bins ,kde=True,kde_kws={"bw":.42}, hist_kws={"rwidth":1}, hist = True, norm_hist = False, label = "Altri documenti")
    
    ax.set_xticks(np.arange(0,10,1))
    # ax = sns.distplot(neg, kde=True, hist = True, norm_hist = False, label = "Altri documenti")
    ax.set(xlim=(0, 6), ylim=(0,0.5))
    ax.set(xlabel="Profondità", ylabel = "Densità di probabilità")
    ax.legend()
    # a_plot.set(ylim=(0, 2000))  
    # ax = sns.distplot(pos)
    plt.show()
    # plt.savefig("csv_links_processing/data/plots/density_plot.png")
