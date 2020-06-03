from sklearn import svm
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import pandas as pd
import joblib
from .plot import generate_svm_plot

def generate_svm(dataset_path = "links_classifiers/data/dataset.csv", load_name = "", kernel_type='rbf'):
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
            "svm" : svm.SVC(probability=True, C=c, kernel=kernel_type).fit(X_train, y_train), 
            "name": "c_{}_{}".format(c, kernel_type).replace('.', '_')
        }

    # generate_svm_plot()
    y_pred = s['svm'].predict(X_test)
    s['score'] = metrics.accuracy_score(y_test, y_pred)
    s['confusion_matrix'] = metrics.confusion_matrix(y_test, y_pred)
    s['f1_score'] = 0 

    for m in ['micro', "macro", "weighted", None]:
        print(metrics.f1_score(y_test, y_pred, average=m))
        
    # for k, v in s.items():
    #     print("{} : {}".format(k, v))
    
    # joblib.dump(s['svm'], "links_classifiers/models/svm/{}.sav".format(s['name']))


    return s['svm']
    