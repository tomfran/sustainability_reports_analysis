import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
import joblib

data = pd.read_csv("../data/dtree_dataset.csv")

X = data[data.columns[:-2]]
Y = data.label

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(X_train,y_train)

# tree.plot_tree(clf.fit(X_train,y_train)) 
filename = '../model/trained_decision_tree.sav'
joblib.dump(clf, filename)

# load the model from disk
load = joblib.load(filename)

y_pred = load.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))