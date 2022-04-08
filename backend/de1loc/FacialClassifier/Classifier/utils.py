# This code was written in reference to the content of UBC's CPSC 340
import numpy as np

def bootstrap(X, y):
    n = len(y)
    new_X = []
    new_y = []
    for i in range(n):
        r = np.random.randint(0, n)
        new_X.append(X[r])
        new_y.append(y[r])
    return np.array(new_X), np.array(new_y)

def gen_dropout(d, dropout_chance):
    a = []
    for i in range(d):
        a.append(True if np.random.binomial(1, 1-dropout_chance) else False)
    return np.array(a)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))