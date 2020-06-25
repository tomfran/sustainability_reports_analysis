from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from sklearn import svm, datasets
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm



def generate_tree_plot(dt, X, Y):
    """Generate the visual representation of the given tree, with relative input and output lists.

    Arguments:
        dt {dict with sklearn decision tree and name} -- Decision tree to plot
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
        "2018\nin filename",
        "2018\nin anchor",
        "2018\nin url"
    ]

    rcParams['figure.figsize'] = 35,16
    tree.plot_tree(dt['tree'].fit(X,Y),filled=True, class_names= classnames, feature_names=features_names, fontsize=13)
    plt.title("Sustainability links decision tree, {}".format(dt['name']))
    plt.savefig("links_classifiers/models/tree/plots/{}.png".format(dt['name']))


def generate_svm_plot(dataset_path = "links_classifiers/data/dataset.csv", c=8.0):
    plt.rcParams.update({'font.size': 8})
    features = [
        "k1_filename",
        "k1_anchor",
        "k1_url",
        "k2_filename",
        "k2_anchor",
        "k2_url",
        "k3_filename",
        "k3_anchor",
        "k3_url",
        "k4_filename",
        "k4_anchor",
        "k4_url",
        "18_filename",
        "18_anchor",
        "18_url"
    ]
    features_names = [
        "sustainability in filename",
        "sustainability in anchor",
        "sustainability in url",
        "environment in filename",
        "environment in anchor",
        "environment in url",
        "balance in filename",
        "balance in anchor",
        "balance in url",
        "report in filename",
        "report in anchor",
        "report in url",
        "2018 in filename",
        "2018 in anchor",
        "2018 in url"
    ]

    data = pd.read_csv(dataset_path)
    X = data[data.columns[:-1]]
    y = data.label

    i = 0
    j = 4

    model = svm.SVC(C = c)

    ll=[(0,6),(0,9),(0,12),(3,6),(3,9),(3,12),(2,6),(2,9),(2,12),(5,6),(5,9),(5,12)]

    fig, ax = plt.subplots(4, 3, figsize=(13,13))
    fig.tight_layout(pad=6.0)
    ax = ax.flatten()
    title = ('Decision surface of linear SVC ')
    for i in range(len(ll)):
        a = ll[i][0]
        b = ll[i][1]
        selected = [features[a], features[b]]
        name1 = features_names[a]
        name2 = features_names[b]

        Xreduced = pd.DataFrame(X, columns=selected)
        clf = model.fit(Xreduced, y)
        X0, X1 = Xreduced[selected[0]], Xreduced[selected[1]]
        xx, yy = make_meshgrid(X0, X1)
        plot_contours(ax[i], clf, xx, yy, cmap=plt.cm.coolwarm, alpha=0.8)
        ax[i].scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
        ax[i].set_ylabel(name1)
        ax[i].set_xlabel(name2)
        ax[i].set_xticks([0,1])
        ax[i].set_yticks([0,1])
        ax[i].set_title('{} / {}'.format(name1, name2))

    plt.savefig("links_classifiers/models/svm/plots/c_{}.png".format(c))

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy

def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out