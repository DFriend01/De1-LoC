from random import randint
import numpy as np
from KNearestNeighbors import KNN
from RandomForest import RandomForest
from SupportVectorMachine import SVM

DATAPOINTS = np.array([[0,0], [1,2], [1,5], [2,4], [2,1],[2,6], [3,7],[3,5],[5,5],[5,7],[3,3],[4,3], [4,4], [5,2],[5,4]])
LABELS = np.array([0,0,0,0,0,1,1,1,1,1,2,2,2,2,2])
MODELS = {
    "KNN": KNN(0),
    "RandomForest": RandomForest(0,drop_out_chance=0.2),
    "SVM": SVM(0)
}

def generateData():
    X = np.concatenate((DATAPOINTS[0:3], DATAPOINTS[5:8], DATAPOINTS[10:13]))
    y = np.concatenate((LABELS[0:3], LABELS[5:8], LABELS[10:13]))
    X_hat = np.concatenate((DATAPOINTS[3:5], DATAPOINTS[8:10], DATAPOINTS[13:]))
    y_hat = np.concatenate((LABELS[3:5], LABELS[8:10], LABELS[13:]))
    return X, y, X_hat, y_hat

def TestModel(model_type):
    X, y, X_hat, y_hat = generateData()
    model = MODELS[model_type]
    model.train(X, y)
    sum = 0
    train_acc =  0
    for i in range(len(y)):
        train_acc += (model.eval(X[i])[0] == y[i])/len(y)
    print(model_type, "train acc: ", train_acc)
    for i in range(len(y_hat)):
        x_hat = X_hat[i]
        expected = y_hat[i]
        pred = model.eval(x_hat)
        sum += expected == pred[0]
    return sum/len(y_hat)

def TestClassifiers():
    knn = TestModel("KNN")
    # knn = None
    rf = TestModel("RandomForest")
    # rf = None
    svm = TestModel("SVM")
    # svm = None
    return knn, rf, svm

if __name__ == '__main__':
    knn, rf, svm = TestClassifiers()
    print("KNN Result")
    print(knn)
    print("RandomForest Result")
    print(rf)
    print("SVM Result")
    print(svm)