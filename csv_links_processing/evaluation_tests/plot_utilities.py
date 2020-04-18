import os
import numpy as np
import matplotlib.pyplot as plt

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
    titles = ["Websites who published", "Websites who published %", \
              "Useful pdf links", "Useful pdf links %", \
              "Average depth", "Link in homepage"]
    ylab = ["Websites number", "Websites percentage", \
            "Pdf number", "Pdf percentage", \
            "Depth", "Websites number"]

    labels = ["1", "2", "3", "4", "5"]
    
    ax.set_ylabel(ylab[i])
    ax.set_xlabel("Evaluation methods")
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


def generate_plot(i, stp):
    a = stp[i][0]
    b = stp[i][1]

    x = np.arange(len(a))  # the label locations
    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars
    rects1 = ax.bar(x - width/2, a, width, label='60 thold')
    rects2 = ax.bar(x + width/2, b, width, label='40 thold')

    add_labels(ax, rects1, rects2, x, i)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))