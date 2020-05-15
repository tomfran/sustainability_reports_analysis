from sklearn import ensemble
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import pandas as pd
import joblib

def generate_forest (dataset_path = "links_classifiers/data/dtree_dataset.csv", load_name = "", n_trees = 20):
    if load_name:
        try:
            t = joblib.load(load_name + ".sav")
            return t
        except Exception:
            print("Could not find tree named %s, generating another one" %load_name)
            pass

    data = pd.read_csv(dataset_path)
    X = data[data.columns[:-1]]
    Y = data.label
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1)
    
    rf= ensemble.RandomForestClassifier(n_estimators=n_trees, criterion="entropy")
    rf.fit(X_train, y_train)

    print("Random forest accuracy: {}" . format(metrics.accuracy_score(y_test, rf.predict(X_test))))

    joblib.dump(rf, "links_classifiers/models/random_forest/{}.sav".format(n_trees))
    return rf