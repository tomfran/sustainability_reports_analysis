from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

def generate_tree_plot(tree, X, Y):
    classnames = ["Negative", "Positive"]

    features_names = [
        "sustainability\nin filename",
        "sustainability\nin anchor",
        "sustainability\nin url",
        "environment\nin filename",
        "environment\nin anchor",
        "environment\nin url",
        "balance\nin filename",
        "balance\nin anchor",
        "balance\nin url",
        "report\nin filename",
        "report\nin anchor",
        "report\nin url",
        "global\nin filename",
        "global\nin anchor",
        "global\nin url",
        "impact\nin filename",
        "impact\nin anchor",
        "impact\nin url",
        "k7\nin filename",
        "k7\nin anchor",
        "k7\nin url",
        "2018\nin filename",
        "2018\nin anchor",
        "2018\nin url"
    ]

    rcParams['figure.figsize'] = 30,15
    tree.plot_tree(tree['tree'].fit(X,Y),filled=True, class_names= classnames, feature_names=features_names, fontsize=13)
    plt.title("Sustainability links decision tree")
    plt.savefig("../model/tree.png",)
# plt.show()