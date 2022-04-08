from Classifier import Classifier
import numpy as np
from scipy import stats

class KNN(Classifier):
    def __init__(self, confidence_threshold, k=3):
        super().__init__(confidence_threshold)
        self.k = k

    #Expects X to be a numpy array of numpy arrays represent the face encoding. Expects y
    #to be a list of strings, where y[i] is the label for encoding X[i]s
    def train(self, X, y):
        self.X = X
        self.y = y

    #Expects x_hat to be a numpy array representing the face encoding. Returns the predicted label.
    def eval(self, x_hat):
        distances = np.full(np.shape(self.y), np.inf)
        preds = []
        for i in range(len(self.y)):
           distances[i] = np.linalg.norm(self.X[i] - x_hat)
        average_distance = 0
        for j in range(self.k):
            point = np.argmin(distances)
            label = self.y[point]
            preds.append(label)
            average_distance+= distances[point]
            distances[point] = np.inf
        average_distance = average_distance / self.k
        pred = stats.mode(preds).mode[0]
        conf = average_distance < self.confidence_threshold
        return pred, conf



    