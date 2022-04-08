import os
import numpy as np
import random
import pickle

from .Classifier.RandomForest import RandomForest

MODELDIR = 'model'
MODEL_FILENAME = 'model'

# Classifier hyperparameters
CONFIDENCE = 0.5
MAX_DEPTH = 140
NUM_TREES = 64
FEATURE_DROPOUT = 0.1

# https://www.geeksforgeeks.org/python-shuffle-two-lists-with-same-order/
def shuffleLists(l1, l2):
    zipped = list(zip(l1, l2))
    random.shuffle(zipped)
    shuffled_l1, shuffled_l2 = zip(*zipped)
    return list(shuffled_l1), list(shuffled_l2)

def getEmbeddingFiles(user_id):
    embedding_paths = [os.path.join(os.path.dirname(__file__), 'embeddings', user_id, f) 
            for f in os.listdir(os.path.join(os.path.dirname(__file__), 'embeddings', user_id))]
    return embedding_paths

def loadEmbeddings(user_id):
    embedding_paths = getEmbeddingFiles(user_id)
    embeddings = [np.load(path) for path in embedding_paths]
    labels = [int(user_id)] * len(embeddings)
    return embeddings, labels

def getEmbeddings():
    uids = os.listdir(os.path.join(os.path.dirname(__file__), 'embeddings'))
    embeddings = []
    labels = []
    for id in uids:
        e, l = loadEmbeddings(id)
        embeddings += e
        labels += l
    embeddings_shuffled, labels_shuffled = shuffleLists(embeddings, labels)
    return np.array(embeddings_shuffled), np.array(labels_shuffled)

def save_model(model):

    # Create model directory if it does not already exist
    if not os.path.exists(os.path.join(os.path.dirname(__file__), MODELDIR)):
        os.makedirs(os.path.join(os.path.dirname(__file__), MODELDIR))
    
    # Save the model
    file = open(os.path.join(os.path.dirname(__file__), MODELDIR, MODEL_FILENAME), 'wb')
    pickle.dump(model, file)
    file.close()

def trainModel():
    embeddings, labels = getEmbeddings()
    classifier = RandomForest(
        confidence_threshold=CONFIDENCE,
        max_depth=MAX_DEPTH,
        drop_out_chance=FEATURE_DROPOUT,
        num_trees=NUM_TREES
    )
    classifier.train(embeddings, labels)
    save_model(classifier)