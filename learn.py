import game
import sys
import csv
import re
import numpy as np
import dstats


from sklearn import svm
#--Pass completion Prob, binary classifier --#
def getCompletionProbModel(passplays):
  X = [e[0:-1] for e in passplays]
  Y = [-1 if e[-1] == 0 else 1 for e in passplays]
  m = svm.SVC(kernel='rbf', probability=True)
  m.fit(X,Y)
  return m




import pylab as pl
from sklearn import neighbors
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score

def learnKNN(xtrain, ytrain, n=5):
    n_neighbors = n
    knc = neighbors.KNeighborsClassifier(n_neighbors, warn_on_equidistant=False, weights='distance')

    kmodel = knc.fit(xtrain,ytrain)
    return kmodel
#y_scores = kmodel.predict(xtest)
#print y_scores

