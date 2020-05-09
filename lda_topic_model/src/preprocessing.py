import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
import re
import sys
from .utilities import filter_frequency, filter_frequency_relevant

csv.field_size_limit(sys.maxsize)

def preprocess(path):
    # read csv with index, entities separated by '_'
    data = pd.read_csv(path, error_bad_lines=False, engine="python", quoting=csv.QUOTE_NONE)
    data = data.drop(['elastic_index'], axis = 1)

    # lowercase all entities and put in entites_processed
    data['entities_processed'] = data['entities'].map(lambda x: x.lower())

    # translate all word in english??
    # divide them in languages and fit lda???
    tf_vectorizer = CountVectorizer(stop_words='english')
    dtm_tf = tf_vectorizer.fit_transform(data['entities_processed'])

    return dtm_tf, tf_vectorizer

def preprocess_freq_count(path, n, m):
    # read csv with index, entities separated by '_'
    data = pd.read_csv(path, error_bad_lines=False, engine="python", quoting=csv.QUOTE_NONE)
    data = data.drop(['elastic_index'], axis = 1)

    # lowercase all entities and put in entites_processed
    data['entities_processed'] = data['entities'].map(lambda x: x.lower())
    
    fd_all = {}
    for row in data['entities_processed']:
        seen = set()
        for w in row.split(" "):
            if w not in seen:
                if w in fd_all:
                    fd_all[w] += 1
                else:
                    fd_all[w] = 1
                seen.add(w)

    data['entities_processed'] = data['entities_processed'].map(lambda x: filter_frequency(x, fd_all, n, m))

    tf_vectorizer = CountVectorizer(stop_words='english')
    dtm_tf = tf_vectorizer.fit_transform(data['entities_processed'])
    return dtm_tf, tf_vectorizer

def preprocess_freq_count_relevant(path, n, m):
    # read csv with index, entities separated by '_'
    data = pd.read_csv(path, error_bad_lines=False, engine="python", quoting=csv.QUOTE_NONE)
    data = data.drop(['elastic_index'], axis = 1)

    # lowercase all entities and put in entites_processed
    data['entities_processed'] = data['entities'].map(lambda x: x.lower())
    
    fd_all = {}
    for row in data['entities_processed']:
        seen = set()
        for w in row.split(" "):
            if w not in seen:
                if w in fd_all:
                    fd_all[w] += 1
                else:
                    fd_all[w] = 1
                seen.add(w)

    data['entities_processed'] = data['entities_processed'].map(lambda x: filter_frequency_relevant(x, fd_all, n, m))

    tf_vectorizer = CountVectorizer(stop_words='english')
    dtm_tf = tf_vectorizer.fit_transform(data['entities_processed'])
    return dtm_tf, tf_vectorizer