from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.neural_network import MLPRegressor
import numpy as np


class nmpcrlcritictransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        self.critic = MLPRegressor(hidden_layer_sizes=(100, 100, )) 
    

    def fit(self, X, y=None):  #X the X vector inputs are all the states and the action vector, the output y 
                                #is the reward/obj function
        #there will not fitting here since the Pipe this will be part of will not fit this estimator.  
        # The critic will be fit seperately
        return self


    def predict(self, X):
        dimensions = X.shape
        return np.hstack((self.critic.predict(X), np.zeros((dimensions[0], dimensions[1] - 1))))


    def transform(self, X):
        return self.predict(X)


    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)