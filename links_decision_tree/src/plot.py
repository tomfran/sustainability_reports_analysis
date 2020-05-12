from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

def generate_tree_plot(dt, X, Y):
    """Generate the visual representation of the given tree, with relative input and output lists.

    Arguments:
        dt {sklearn decision tree} -- Decision tree to plot
        X {list} -- input top the decision tree
        Y {list} -- ground truth labels
    """
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
        # "global\nin filename",
        # "global\nin anchor",
        # "global\nin url",
        # "impact\nin filename",
        # "impact\nin anchor",
        # "impact\nin url",
        # "k7\nin filename",
        # "k7\nin anchor",
        # "k7\nin url",
        "2018\nin filename",
        "2018\nin anchor",
        "2018\nin url"
    ]

    rcParams['figure.figsize'] = 35,16
    tree.plot_tree(dt['tree'].fit(X,Y),filled=True, class_names= classnames, feature_names=features_names, fontsize=13)
    plt.title("Sustainability links decision tree")
    plt.savefig("links_decision_tree/model/tree/tree.png",)
