import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
import re
import sys

csv.field_size_limit(sys.maxsize)

def preprocess(path):
    # read csv with index, entities separated by '_'
    data = pd.read_csv(path, error_bad_lines=False, engine="python", quoting=csv.QUOTE_NONE)
    data = data.drop(['elastic_index'], axis = 1)

    # lowercase all entities and put in entites_processed
    data['entities_processed'] = data['entities'].map(lambda x: x.lower())

    tf_vectorizer = CountVectorizer(stop_words='english')
    dtm_tf = tf_vectorizer.fit_transform(data['entities_processed'])

    return dtm_tf, tf_vectorizer