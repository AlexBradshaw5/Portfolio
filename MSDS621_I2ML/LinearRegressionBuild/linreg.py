import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

def normalize(X): # creating standard variables here (u-x)/sigma
    if isinstance(X, pd.DataFrame):
        for c in X.columns:
            if is_numeric_dtype(X[c]):
                u = np.mean(X[c])
                s = np.std(X[c])
                X[c] = (X[c] - u) / s
        return
    for j in range(X.shape[1]):
        u = np.mean(X[:,j])
        s = np.std(X[:,j])
        X[:,j] = (X[:,j] - u) / s

def loss_gradient(X, y, B, lmbda):
    return np.dot((-np.transpose(X)), y - np.dot(X, B))

def loss_ridge(X, y, B, lmbda):
    pass
    #return np.dot(np.transpose(y - X @ B), y - X @ B) + np.dot(lmbda, B.T @ B)

def loss_gradient_ridge(X, y, B, lmbda):
    return np.dot(-np.transpose(X), y - np.dot(X, B)) + np.dot(lmbda, B)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def log_likelihood(X, y, B,lmbda):
    pass

def log_likelihood_gradient(X, y, B, lmbda):
    return np.dot(-np.transpose(X), y - sigmoid(np.dot(X, B)))

def minimize(X, y, loss_gradient,
              eta=0.00001, lmbda=0.0,
              max_iter=1000, addB0=True,
              precision=1e-9):
    # check X and y dimensions and set n and p to X dimensions
    if X.ndim != 2:
        raise ValueError("X must be n x p for p features")
    n, p = X.shape
    if y.shape != (n, 1):
        raise ValueError(f"y must be n={n} x 1 not {y.shape}")

    # if we are doing linear or logistic regression, we want to estimate B0 by adding a column of 1s and increase p by 1
    # for Ridge regression we will set addB0 to False and estimate B0 as part of the RidgeRegression621 fit method
    if addB0:
        X0 = np.ones((n,1))
        X = np.hstack((X0, X))
        p += 1

    # initiate a random vector of Bs of size p
    B = np.random.random_sample(size=(p, 1)) * 2 - 1  # make between [-1,1)

    # start the minimization procedure here
    prev_B = B
    eps = 1e-5 # prevent division by 0
    
    # remember we need to retain the history of the gradients to use as part of our iteration procedure
    # remember to check stopping condition L2-norm of the gradient <= precision
    
    h = 0
    for i in range(max_iter):
        grad = loss_gradient(X, y, B, lmbda)
        if(np.linalg.norm(grad) <= precision):
            break
        h += np.square(grad)
        B = B - eta/np.sqrt(h+eps) * grad
    return B
        

class LinearRegression621: 
    def __init__(self,
                 eta=0.00001, lmbda=0.0,
                 max_iter=1000):
        self.eta = eta
        self.lmbda = lmbda
        self.max_iter = max_iter

    def predict(self, X):
        n = X.shape[0]
        B0 = np.ones(shape=(n, 1))
        X = np.hstack([B0, X])
        return np.dot(X, self.B)

    def fit(self, X, y):
        self.B = minimize(X, y,
                          loss_gradient,
                          self.eta,
                          self.lmbda,
                          self.max_iter)


class LogisticRegression621:
    "Use the above class as a guide."
    
    def __init__(self,
                 eta=0.00001, lmbda=0.0,
                 max_iter=1000):
        self.eta = eta
        self.lmbda = lmbda
        self.max_iter = max_iter
    
    def predict_proba(self, X):
        n = X.shape[0]
        B0 = np.ones(shape=(n, 1))
        X = np.hstack([B0, X])
        return sigmoid(np.dot(X, self.B))
        """
        Compute the probability that the target is 1. Basically do
        the usual linear regression and then pass through a sigmoid.
        """
        
    def predict(self, X):
        probas = self.predict_proba(X)
        return np.round(probas)
        """
        Call self.predict_proba() to get probabilities then, for each x in X,
        return a 1 if P(y==1,x) > 0.5 else 0.
        """

    def fit(self, X, y):
        self.B = minimize(X, y,
                          log_likelihood_gradient,
                          self.eta,
                          self.lmbda,
                          self.max_iter)


class RidgeRegression621:
    def __init__(self,
                 eta=0.00001, lmbda=0.0,
                 max_iter=1000):
        self.eta = eta
        self.lmbda = lmbda
        self.max_iter = max_iter
    "Use the above classes as a guide."
    def predict(self, X):
        n = X.shape[0]
        B0 = np.ones(shape=(n, 1))
        X = np.hstack([B0, X])
        return np.dot(X, self.B)
    
    def fit(self, X, y):
        self.B = minimize(X, y,
                          loss_gradient_ridge,
                          self.eta,
                          self.lmbda,
                          self.max_iter, addB0 = False)
        #self.B[0] = np.mean(y)
        self.B = np.insert(self.B, 0, np.mean(y))
        