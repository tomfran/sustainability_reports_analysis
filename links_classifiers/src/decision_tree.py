import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn import tree
from sklearn import metrics
import joblib
# from .plot import generate_tree_plot

def generate_tree(dataset_path = "links_classifiers/data/dtree_dataset.csv", load_name = ""):

    """Generate a decision tree to decide wether a link is referring to a sustainability report or not.
    

    Keyword Arguments:
        dataset_path {str} -- Path to the dataset to use (default: {"links_classifiers/data/dtree_dataset.csv"})
        load_name {str} -- Model to load and return (default: {""})

    Returns:
        Best decision tree generated
    """
    
    if load_name:
        try:
            t = joblib.load("links_classifiers/models/tree/"+ load_name + ".sav")
            return t
        except Exception:
            print("Could not find tree named %s, generating another one" %load_name)
            pass

    data = pd.read_csv(dataset_path)
    X = data[data.columns[:-1]]
    Y = data.label
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1)

    #generate some decision trees to see what's the best one
    dtrees = [
        {
            "tree" : tree.DecisionTreeClassifier(min_samples_leaf=ms,
                                                 criterion=criterion, 
                                                 max_depth=depth).fit(X_train, y_train),  
            "name": "%s_%d_%d" %(criterion[0], ms, depth)
        }
        for ms in [i for i in range(2,21,2)]
        for criterion in ["gini", "entropy"]
        for depth in [i for i in range(2,11,2)]
    ]

    # make predictions for all trees, and check the accuracy
    predictions = [d['tree'].predict(X_test) for d in dtrees]
    scores = [metrics.accuracy_score(y_test, p) for p in predictions]

    # add scores to tree list
    i = 0
    for d in dtrees:
        d['score'] = scores[i]
        i += 1
    
    #order the trees based on accuracy and save the first one
    dtrees.sort(key=lambda x : x['score'], reverse = True)
    t = dtrees[0]
    joblib.dump(t['tree'], "links_classifiers/models/tree/" + t['name']+'.sav')
    
    return t['tree']