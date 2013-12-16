from sklearn.svm import SVR
import numpy as np
import learn
import team
from sklearn import linear_model
import re
import json
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
import data_ops

Xall = []
teams = []

RM = data_ops.RunData('./data/2013_nfl_pbp_through_wk_12.csv')
Xa, Yalltrain = RM.RunTrainData()
#Xf = [e[0:-2] for e in Xa]
Xalltrain = []
if True:
  for x in Xa:
      q = x[4]/4.0
      f = x[5]/10.0
      y = x[6]/100.0
      Xalltrain.append(x[0:3]+[q]+[f]+[y]+x[7:])
else:
  Xalltrain = Xa
    


clf =  linear_model.LogisticRegression(C=1.0, penalty='l1')# tol=1e-6)
model = clf.fit(Xalltrain,Yalltrain)

from sklearn.metrics import average_precision_score
y_true = Yalltrain 
y_scores = model.predict(Xalltrain)  


from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
from sklearn import linear_model
Xdata = Xalltrain
Ydata = Yalltrain
print Xdata[0]
def evalRegressorOnTrainingData(regressor, Xdata, Ydata):
    m = regressor.fit(Xdata, Ydata)
    y_scores = m.predict(Xdata)
    eval_regres(y_true, y_scores)
#    print "------"+str(regressor)+"--------"
    print "Score: " + str(m.score(Xalltrain,Yalltrain))
    print "Mean absolute error "+  str(mean_absolute_error(y_true, y_scores))
    print "Mean squared error " + str(mean_squared_error(y_true,y_scores))
    print "Explained variance score " + str(explained_variance_score(y_true,y_scores))
    print "r2 score" + str(r2_score(y_true, y_scores))
#    print m.coef_
 

def eval_regres(y_true, y_pred):
    t = 0.0
    tc = 0.0
    for i in range(len(y_true)):
        t+=1
        if abs(y_true[i] - y_pred[i]) <=1:
           tc +=1
    print "Percent correct: "+ str(tc/t)

#print "-----PERCEPTRON REGRESSION-----"
#evalRegressorOnTrainingData(linear_model.Perceptron(), Xdata, Ydata)
#print "-----Partial fit PERCEPTRON REGRESSION-----"

print "-----SGD REGRESSION-----"
print "Fails because of overflow/undeflow"
#evalRegressorOnTrainingData(linear_model.SGDRegressor(), Xdata, Ydata)



print "-----LOGISTIC REGRESSION-----"
print "L1:"
evalRegressorOnTrainingData(linear_model.LogisticRegression(C=1.0, penalty='l1',dual=False,fit_intercept=True,tol=0.0001), Xdata, Ydata)
print "L2:"
evalRegressorOnTrainingData(linear_model.LogisticRegression(C=1.0, penalty='l2'), Xdata, Ydata)
print "-----LINEAR REGRESSION-----"
evalRegressorOnTrainingData(linear_model.LinearRegression(), Xdata, Ydata)
print "-----RIDGE REGRESSION-----"
evalRegressorOnTrainingData(linear_model.Ridge (alpha = .5), Xdata, Ydata)
print "-----BAYESIAN RIDGE REGRESSION-----"
evalRegressorOnTrainingData(linear_model.BayesianRidge(), Xdata, Ydata)
#print "-----ARD REGRESSION-----"
#evalRegressorOnTrainingData(linear_model.ARDRegression(), Xdata, Ydata)




