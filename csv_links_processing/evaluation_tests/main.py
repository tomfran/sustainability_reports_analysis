import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def main():
    total_websites = 0
    total_pdfs = 0
    
    websites = [[],[]] 
    websites_perc = [[],[]] 
    pdf_links = [[],[]] 
    pdf_links_perc = [[],[]] 
    depth = [[],[]] 
    home = [[],[]] 
    
    stats_list = ["data/"+l for l in sorted(os.listdir("data/"))]
    print(stats_list)
    for f in stats_list:
        with open(f, "r") as s:
            l = s.readlines()
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

    titles = ["Websites who published", "Websites who published %", \
              "Useful pdf links", "Useful pdf links %", \
              "Average depth", "Link in homepage"]
    ylab = ["Websites number", "Websites percentage", \
            "Pdf number", "Pdf percentage", \
            "Depth", "Websites number"]
    
    l = [i for i in range(1,len(stats_list)+1)]

    labels = ["1", "2", "3", "4", "5"]
    count = 0
    for s in stp:
        a = s[0]
        b = s[1]

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, a, width, label='60 thold')
        rects2 = ax.bar(x + width/2, b, width, label='40 thold')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel(ylab[count])
        ax.set_xlabel("Evaluation methods")
        ax.set_title(titles[count])
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        autolabel(rects1, ax)
        autolabel(rects2, ax)

        # fig.tight_layout()
        # plt.show()
        plt.savefig('graphs/%d.png' %(count), dpi=300, quality=100)
        count += 1

if __name__ == "__main__":
    main()
