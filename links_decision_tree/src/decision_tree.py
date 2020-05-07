import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import joblib
import matplotlib.pyplot as plt

data = pd.read_csv("../data/dtree_dataset.csv")

X = data[data.columns[:-2]]
Y = data.label

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=1)

clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(X_train,y_train)


dtrees = [
    tree.DecisionTreeClassifier(min_samples_leaf=ms, criterion=criterion, max_depth=depth).fit(X_train, y_train) 
    for ms in [3,4]
    for criterion in ["gini", "entropy"]
    for depth in [3,4]
]
predictions = [d.predict(X_test) for d in dtrees]
scores = [metrics.accuracy_score(y_test, p) for p in predictions]
dt_names = [ "%s_%d_%d" %(criterion[0], ms, depth)
    for ms in [3,4]
    for criterion in ["gini", "entropy"]
    for depth in [3,4]
]


plt.plot(scores, "*")
plt.ylabel("Accuracy")
plt.xlabel("Models")
plt.xticks(range(len(dt_names)), dt_names)
plt.show()

# # tree.plot_tree(clf.fit(X_train,y_train)) 
# filename = '../model/trained_decision_tree.sav'
# joblib.dump(clf, filename)

# # load the model from disk
# load = joblib.load(filename)

# y_pred = load.predict(X_test)
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred))