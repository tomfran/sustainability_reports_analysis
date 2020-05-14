from sklearn import svm
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import pandas as pd
import joblib
from .plot import generate_svm_plot

def generate_svm(dataset_path = "links_classifiers/data/dtree_dataset.csv", load_name = ""):
    if load_name:
        try:
            t = joblib.load("links_classifiers/models/svm/"+ load_name + ".sav")
            return t
        except Exception:
            print("Could not find svm named %s, generating another one" %load_name)
            pass

    data = pd.read_csv(dataset_path)
    X = data[data.columns[:-1]]
    Y = data.label
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=1)
    
    c = 8.0

    s = {
            "svm" : svm.SVC(probability=True, C=c).fit(X_train, y_train), 
            "name": "c_{}".format(c).replace('.', '_')
        }

    generate_svm_plot()

    s['score'] = metrics.accuracy_score(y_test, s['svm'].predict(X_test))
    
    joblib.dump(s['svm'], "links_classifiers/models/svm/{}.sav".format(s['name']))

    return s['svm']
    