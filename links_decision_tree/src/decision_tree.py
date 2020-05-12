import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn import tree
from sklearn import metrics
import joblib
# from .plot import generate_tree_plot

def generate_tree(dataset_path = "links_decision_tree/data/dtree_dataset.csv"):
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
        for ms in [2, 4, 6, 8]
        for criterion in ["gini", "entropy"]
        for depth in [3,4,5,6]
    ]

    # make predictions for all trees, and check the accuracy
    predictions = [d.predict(X_test) for d['tree'] in dtrees]
    scores = [metrics.accuracy_score(y_test, p) for p in predictions]

    # add scores to tree list
    i = 0
    for d in dtrees:
        d['score'] = scores[i]
        i += 1
    
    #order the trees based on accuracy and save the first one
    dtrees.sort(key=lambda x : x['score'], reverse = True)
    t = dtrees[0]
    joblib.dump(t['tree'], "../model/" + t['name']+'.sav')
    
    return t