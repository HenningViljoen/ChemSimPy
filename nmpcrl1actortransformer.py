from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.neural_network import MLPRegressor
import numpy as np


class nmpcrl1actortransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, astate1thirdlength, astatelength):
        self.state1thirdlength = astate1thirdlength
        self.statelength = astatelength
        self.actor = MLPRegressor(hidden_layer_sizes=(100, 100, ))
    

    def fit(self, X, y=None):  #X the X vector inputs are all the states, the output y are the same states, 
                                #as well as the action vector
        self.actor.fit(X, y[:, self.statelength:])
        return self


    def predict(self, X):
        return np.hstack((X, self.actor.predict(X)))


    def transform(self, X):
        actoroutput = self.actor.predict(X)
        actoroutputshape = actoroutput.shape
        if len(actoroutputshape) == 1: actoroutput = actoroutput.reshape(-1, 1)
        transformoutput = np.hstack((X, actoroutput))
        return transformoutput


    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)
    

