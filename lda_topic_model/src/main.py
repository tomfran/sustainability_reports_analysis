from .preprocessing import preprocess
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import os

def trainLDA(input_path):
    dtm_tf, tf_vectorizer = preprocess(input_path)
    topics = 10
    words = 10

    lda = LatentDirichletAllocation(n_components = topics, random_state=0)
    lda.fit(dtm_tf)

if __name__ == "__main__":
    trainLDA()