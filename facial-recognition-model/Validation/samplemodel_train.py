import os
import sys
import random
import numpy as np
import pickle

# Append path so we can access parent folders
sys.path.append('../')

from Classifier.RandomForest import RandomForest

CATEGORIES = ['Devon', 'Declan', 'Harshil', 'Aswin', 'other']
CONFIDENCE = 0.5
MAX_DEPTH = 140
NUM_TREES = 64
FEATURE_DROPOUT = 0.1

MAPPINGS = {'other' : 0, 'Devon' : 1, 'Declan' : 2, 'Harshil' : 3, 'Aswin' : 4}
def mapLabels(labels):
    for i in range(len(labels)):
        labels[i] = MAPPINGS[labels[i]]
    return labels

# https://www.geeksforgeeks.org/python-shuffle-two-lists-with-same-order/
def shuffleLists(l1, l2):
    zipped = list(zip(l1, l2))
    random.shuffle(zipped)
    shuffled_l1, shuffled_l2 = zip(*zipped)
    return list(shuffled_l1), list(shuffled_l2)


def getDataPaths(categories):
    embedding_data = []
    labels = []

    for c in categories:
        data = [os.path.join('embeddings', c, f) for f in os.listdir(os.path.join('embeddings', c))]
        embedding_data += data
        labels += [c] * len(os.listdir(os.path.join('embeddings', c)))

    embedding_data_shuffled, labels_shuffled = shuffleLists(embedding_data, labels)
    return embedding_data_shuffled, mapLabels(labels_shuffled)


def getEmbeddings(categories):
    embedding_data_paths, labels = getDataPaths(categories)
    embeddings = [np.load(e) for e in embedding_data_paths]
    return np.array(embeddings), np.array(labels)

if __name__ == '__main__':
    embeddings, labels = getEmbeddings(CATEGORIES)
    classifier = RandomForest(
        confidence_threshold=CONFIDENCE,
        max_depth=MAX_DEPTH,
        drop_out_chance=FEATURE_DROPOUT,
        num_trees=NUM_TREES
    )

    classifier.train(embeddings, labels)

    if not os.path.exists('samplemodel/'):
        os.makedirs('samplemodel/')

    file = open('samplemodel/model', 'wb')
    pickle.dump(classifier, file)
    file.close()
