from sklearn import svm
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import pandas as pd
import joblib
import matplotlib.pyplot as plt 
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

    print(list(s['svm'].predict_proba(X_test)[:,1]))
    return
    stp = []
    i = -1
    x = [2, 1, 0.5, 0.1, 0.05, 0.01, 0.05]
    for t in [0.5, 0.6, 0.7, 0.8, 0.9]:
        i += 1
        y_pred = (s['svm'].predict_proba(X_test)[:,1] >= t).astype(bool)
        print(f"Threshold: {t}\nConfusion Matrix: ")
        for r in metrics.confusion_matrix(y_test, y_pred):
            print(r)
        print("")
        ll = []
        for b in x:
            # print(metrics.accuracy_score(y_test, y_pred))
            ll.append(metrics.fbeta_score(y_test, y_pred, average='macro', beta = b))
        stp.append(ll)
        # dd = { k: v for k, v in sorted(dd.items(), key = lambda x: x[1])}
        # for k,v in dd.items():
        #     print(f"{k} : {v}")
    print(stp)

    labels = ["0.5", "0.6", "0.7", "0.8", "0.9"]
    i = -1
    plt.grid()
    for p in stp:
        i+=1
        plt.plot(x, p, label=labels[i])
    plt.legend()
    plt.xlabel("beta")
    plt.ylabel("Fbeta")
    plt.show()

    # # print(s['svm'].predict_proba(X_test))
    # # generate_svm_plot()
    # a = 0.8
    # for a in range(11):
    #     k = a/10    
    #     print(f"TSH: {k}")
    #     # y_pred = s['svm'].predict(X_test)
    #     for i in range(21):
    #         print(f"\tbeta: {i/10} fbeta_score : {metrics.fbeta_score(y_test, y_pred, average='micro', beta = i/10)}")

    # s['score'] = metrics.accuracy_score(y_test, y_pred)
    # s['confusion_matrix'] = metrics.confusion_matrix(y_test, y_pred)
    # print(s)





    # for k, v in s.items():
    #     print("{} : {}".format(k, v))
    
    # joblib.dump(s['svm'], "links_classifiers/models/svm/{}.sav".format(s['name']))


    return s['svm']
    