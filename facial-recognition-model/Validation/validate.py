from cgi import test
import os
import sys
import numpy as np
import pandas as pd
import random
import time
from tqdm import tqdm

# Append path so we can access parent folders
sys.path.append('../')

# Import ML models to validate
from Classifier.KNearestNeighbors import KNN
from Classifier.RandomForest import RandomForest

CATEGORIES = ['other', 'Devon', 'Declan', 'Harshil', 'Aswin']
MAPPINGS = {'other' : 0, 'Devon' : 1, 'Declan' : 2, 'Harshil' : 3, 'Aswin' : 4}


def mapLabels(labels):
    for i in range(len(labels)):
        labels[i] = MAPPINGS[labels[i]]
    return labels


def secondsToHMS(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    timestr = f"{int(h):d}:{int(m):2d}:{int(s):02d}"
    return timestr

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


def fold(categories, n_folds):
    folds = []
    folds_labels = []

    embeddings, labels = getDataPaths(categories)

    split = int(len(embeddings) / n_folds)

    for i in range(0, len(embeddings), split):
        training_data = [np.load(e) for e in (embeddings[:i] + embeddings[i+split:])]
        training_labels = (labels[:i] + labels[i+split:])
        testing_data = [np.load(e) for e in embeddings[i:i+split]]
        testing_labels = labels[i:i+split]

        folds.append([training_data, testing_data])
        folds_labels.append([training_labels, testing_labels])

    return folds, folds_labels


def validate_KNN(folds, categories):
    test_k = [1,2,5,10,20,30,50,80,100,120,140,160]
    confidence = 1
    results = []

    pbar = tqdm(desc='KNN Validation', total=len(test_k)*len(folds))

    for k in test_k:
        knn = KNN(confidence_threshold=confidence, k=k)
        average_accuracy = 0

        avg_training_time = 0
        avg_eval_time = 0
        for f in range(len(folds)):
            start_time = time.time()
            knn.train(np.array(folds[f][0]), np.array(categories[f][0]))
            avg_training_time += (time.time() - start_time)

            accuracy = 0
            for i, embedding in enumerate(folds[f][1]):
                start_time = time.time()
                pred, conf = knn.eval(embedding)
                avg_eval_time += (time.time() - start_time)

                if (pred == categories[f][1][i]) and (conf):
                    accuracy += 1

            average_accuracy += (accuracy / len(folds[f][1]))
            pbar.update(1)

        average_accuracy /= len(folds)
        avg_training_time /= len(folds)
        avg_eval_time /= (len(folds) * len(folds[0][1]))
        results.append([k, average_accuracy, secondsToHMS(avg_training_time), secondsToHMS(avg_eval_time)])

    pbar.close()

    # Save the results
    if not os.path.exists('results/'):
        os.makedirs('results/')

    colnames = ['k', 'Average Accuracy', 'Average Training Time', 'Average Evaluation Time']
    df = pd.DataFrame(data=results, columns=colnames)
    df.to_csv('results/knn_validation_results.csv')


def validate_RandomForest(folds, categories):
    test_max_depth = [120, 140]
    test_feature_dropout = [0.05, 0.1]
    test_num_models = [64]
    test_confidence = [0.4, 0.5]
    results = []

    pbar = tqdm(
        desc='Random Forest Validation', 
        total=len(test_max_depth)*len(test_feature_dropout)*len(test_num_models)*len(test_confidence)*len(folds)
    )

    for max_depth in test_max_depth:
        for feature_dropout in test_feature_dropout:
            for num_models in test_num_models:
                for confidence in test_confidence:
                    randForest = RandomForest(
                        confidence_threshold=confidence,
                        max_depth=max_depth,
                        drop_out_chance=feature_dropout,
                        num_trees=num_models
                    )
                    average_accuracy = 0
                    avg_training_time = 0
                    avg_eval_time = 0
                    for f in range(len(folds)):
                        start_time = time.time()
                        randForest.train(np.array(folds[f][0]), np.array(categories[f][0]))
                        avg_training_time += (time.time() - start_time)

                        accuracy = 0
                        for i, embedding in enumerate(folds[f][1]):
                            if embedding is not None:
                                start_time = time.time()
                                pred, conf = randForest.eval(embedding)
                                avg_eval_time += (time.time() - start_time)
                                if (pred == categories[f][1][i]) and (conf):
                                    accuracy += 1

                        average_accuracy += (accuracy / len(folds[f][1]))
                        pbar.update(1)

                    average_accuracy /= len(folds)
                    avg_training_time /= len(folds)
                    avg_eval_time /= (len(folds) * len(folds[0][1]))
                    results.append([max_depth, feature_dropout, num_models, confidence, average_accuracy, secondsToHMS(avg_training_time), secondsToHMS(avg_eval_time)])

    pbar.close()

    # Save the results
    if not os.path.exists('results/'):
        os.makedirs('results/')

    colnames = [
        'Max Depth',
        'Feature Dropout',
        'Num Trees',
        'Confidence Threshold',
        'Average Accuracy',
        'Average Training Time',
        'Average Eval Time'
    ]

    df = pd.DataFrame(data=results, columns=colnames)
    df.to_csv('results/randomforest_validation_results.csv')


if __name__ == '__main__':
    n_folds = 5
    folds, categories = fold(CATEGORIES, n_folds)
    validate_KNN(folds, categories)
    validate_RandomForest(folds, categories)
