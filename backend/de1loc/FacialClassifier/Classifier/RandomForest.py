import numpy as np
from scipy import stats
from .utils import bootstrap, gen_dropout
from .Classifier import Classifier

def entropy(p):
    plogp = 0*p
    plogp[p>0] = p[p>0] * np.log(p[p>0])
    return -np.sum(plogp)

def infogain(p, p_yes, p_no, prob_yes):
    entropy_total = entropy(p)
    entropy_yes = entropy(p_yes)
    entropy_no = entropy(p_no)
    prob_no =  1 - prob_yes
    return entropy_total - prob_yes * entropy_yes - prob_no * entropy_no

class RandomForest(Classifier):
    def __init__(self, confidence_threshold, max_depth=100, drop_out_chance=0, num_trees=32):
        super().__init__(confidence_threshold)
        self.max_depth = max_depth
        self.drop_out_chance = drop_out_chance
        self.num_trees = num_trees
        self.trees = []
        self.keep_features = []
        for i in range(num_trees):
            self.trees.append(DecisionTree(max_depth))
    def train(self, X, y):
        n, d = X.shape
        for i in range(self.num_trees):
            if self.drop_out_chance != 0:
                self.keep_features.append(gen_dropout(d, self.drop_out_chance))
            else:
                self.keep_features.append(np.full(d, True))
            bs_X, bs_y = bootstrap(X[:,self.keep_features[i]], y)
                
            self.trees[i].train(bs_X, bs_y)
    def eval(self, x_hat):
        preds=[]
        for i in range(self.num_trees):
            preds.append(self.trees[i].eval(x_hat[self.keep_features[i]]))
        count = np.bincount(preds)
        pred = np.argmax(count)
        num_correct = count[pred]
        return pred, (num_correct/self.num_trees >= self.confidence_threshold)


class DecisionTree(Classifier):
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.isLeaf = max_depth == 0
    def train(self, X, y):
        n, d = X.shape
        count = np.bincount(y)
        p = count / np.sum(count)

        best_score = 0
        self.splitting_dim = None
        self.splitting_val = None
        self.yes_label = np.argmax(count)
        self.no_label = None

        if np.unique(y).size <= 1:
            self.isLeaf = True
            return

        yes_X = None
        yes_y = None
        no_X = None
        no_y = None

        for i in range(d):
            values = np.unique(X[:,i])
            for value in values:
                condition_check_yes = X[:, i] >= value
                condition_check_no = X[:, i] < value
                count_yes = np.bincount(y[condition_check_yes])
                count_no = np.bincount(y[condition_check_no])


                p_yes = count_yes / np.sum(count_yes)
                p_no = count_no / np.sum(count_no)
                prob_yes = np.sum(condition_check_yes)
                score = infogain(p, p_yes, p_no, prob_yes)
                if score > best_score:
                    best_score = score
                    self.splitting_dim = i
                    self.splitting_val = value
                    if (self.isLeaf):
                        self.yes_label = np.argmax(count_yes)
                        self.no_label = np.argmax(count_no)
                    else:
                        yes_X = X[condition_check_yes]
                        yes_y = y[condition_check_yes]
                        no_X = X[condition_check_no]
                        no_y = y[condition_check_no]
        if (self.splitting_dim is not None):
            self.yes_model = DecisionTree(self.max_depth - 1)
            self.no_model = DecisionTree(self.max_depth - 1)
            self.yes_model.train(yes_X, yes_y)
            self.no_model.train(no_X, no_y)
    

    def eval(self, x_hat):
        #x_hat is being weirdly converted into a list of list, this fixes that
        x_hat = np.array(x_hat).flatten()
        if(self.splitting_dim == None):
            return self.yes_label
        
        if(x_hat[self.splitting_dim] >= self.splitting_val):
            return self.yes_label if self.isLeaf else self.yes_model.eval(x_hat)
        return self.no_label if self.isLeaf else self.no_model.eval(x_hat)
