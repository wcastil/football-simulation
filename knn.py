import numpy as np
import pylab as pl
from sklearn import neighbors
import time 
import data_ops
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score
from sklearn import cross_validation as V

#xtrain,xtest,ytrain,ytest = testSet.holdOutTeamData('CIN')
RM = data_ops.RunData('./data/2013_nfl_pbp_through_wk_12.csv')
XT, YT = RM.RunTrainData(fname='./data/2013_nfl_pbp_through_wk_12.csv')

def EvalKNN(XT, YT, p=0.25, n=5):
    xtrain,xtest,ytrain,ytest = V.train_test_split(XT,YT, test_size=p, random_state=0)
    n_neighbors = n
    knc = neighbors.KNeighborsClassifier(n_neighbors, warn_on_equidistant=False, \
        weights='distance')
    kmodel = knc.fit(xtrain,ytrain) 
    y_scores = kmodel.predict(xtest)
  #  print "knc Train error: " + str(kmodel.score(xtrain, ytrain))
   # print "knc Test error: " + str(kmodel.score(xtest, ytest))

   # print "Predicting test set"
  #  print "Score: " +str(kmodel.score(xtest,ytest))
    eval_regres(ytest,y_scores)
   # print y_scores[0:10]
    #print ytest[0:10]

#print "Mean absolute error "+  str(mean_absolute_error(ytest, y_scores))
#print "Mean squared error " + str(mean_squared_error(ytest,y_scores))
 #   print "Explained variance score " + str(explained_variance_score(ytest,y_scores))
#    print "r2 score" + str(r2_score(ytest, y_scores))

def EvalKNNRegressor(XT,YT,p=0.25,weights='uniform', n=5):
    xtrain,xtest,ytrain,ytest = V.train_test_split(XT,YT, test_size=p, random_state=0)
    knn = neighbors.KNeighborsRegressor(n, weights, warn_on_equidistant=False)
    print "Learning KNN model with "+str(weights)+" weights "
    kmodel = knn.fit(xtrain,ytrain)
    y_scores = kmodel.predict(xtest)
    print "knr Train error: " + str(kmodel.score(xtrain, ytrain))
    print "knr Test error: " + str(kmodel.score(xtest, ytest))
    eval_regres(ytest,y_scores)
    


ntests = []
def eval_regres(y_true, y_pred):
    t = 0.0
    tc = 0.0

    for i in range(len(y_true)):
        t+=1
        if abs(y_true[i] - y_pred[i]) <=1:
           tc +=1
    ntests.append(tc/t)
    print "Percent correct: "+ str(tc/t)

print "---With Defense stats"
EvalKNN(XT,YT)
Xnew = []
for i in range(len(XT)):
    Xnew.append(XT[i][0:-2])

print "---Without defense stats:"
EvalKNN(Xnew, YT)

print "---KNN Regressor"
print EvalKNNRegressor(XT,YT,0.25,n=20)

#print "Find best n"
#for i in range(1,100):
 #   EvalKNN(XT,YT, 0.25, n=i)

#YT.append(XT[i].pop())
#print max(ntests), ntests.index(max(ntests))+1

def EvalKNNRadius(XT,YT,p=0.25,weights='uniform'):
    xtrain,xtest,ytrain,ytest = V.train_test_split(XT,YT, test_size=p, random_state=0)
    knn = neighbors.RadiusNeighborsClassifier(radius=30, weights=weights)
    print "Learning KNN model with "+str(weights)+" weights "
    kmodel = knn.fit(xtrain,ytrain)
    y_scores = kmodel.predict(xtest)
    print "k-radius Train error: " + str(kmodel.score(xtrain, ytrain))
    print "k-radius Test error: " + str(kmodel.score(xtest, ytest))
    eval_regres(ytest,y_scores)

#EvalKNNRadius(XT,YT)

#--Pass KNN--#
def EvalPasses():
  for tm in map(str,data_ops.rosters.keys()):
      PM = data_ops.PassData('./data/2013_nfl_pbp_through_wk_12.csv')
      XT= PM.PassTrainData(fname='./data/2013_nfl_pbp_through_wk_12.csv', teamname=tm)
      YT = []
      for i in range(len(XT)):
         YT.append(XT[i][-1])
#--Evaluate KNN with yardage --#
      EvalKNN(XT,YT,n=3)
      print tm+": "+str(ntests[-1])
      print "Average error: " + str( sum(ntests)/float(len(ntests)))


def EvalTeamRun():
  for tm in map(str,data_ops.rosters.keys()):
      RM = data_ops.RunData('./data/2013_nfl_pbp_through_wk_12.csv')
      XT,YT= RM.RunTrainData(fname='./data/2013_nfl_pbp_through_wk_12.csv', teamname=tm)
      #for i in range(len(XT)):
#        YT.append(XT[i][-1])
      #    YT.append(XT[i].pop())
#--Evaluate KNN with yardage --#
      EvalKNN(XT,YT,n=21)
      print tm+": "+str(ntests[-1])
      print "Average error: " + str( sum(ntests)/float(len(ntests)))


def EvalAllRun():
      RM = data_ops.RunData('./data/2013_nfl_pbp_through_wk_12.csv')
      XT,YT= RM.RunTrainData(fname='./data/2013_nfl_pbp_through_wk_12.csv')
      #for i in range(len(XT)):
#        YT.append(XT[i][-1])
      #    YT.append(XT[i].pop())
#--Evaluate KNN with yardage --#
      EvalKNN(XT,YT,n=21)
      print "Average error: " + str( sum(ntests)/float(len(ntests)))
#EvalTeamRun()

from sklearn import svm as SVM
from sklearn.svm import SVR
def EvalRUNwithSVM():
      p=0.25
      RM = data_ops.RunData('./data/2013_nfl_pbp_through_wk_12.csv')
      XT,YT= RM.RunTrainData(fname='./data/2013_nfl_pbp_through_wk_12.csv',teamname='SF')
      xtrain,xtest,ytrain,ytest = V.train_test_split(XT,YT, test_size=p, random_state=0)
      oc = SVM.SVC(kernel='rbf', probability=True)
      svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
      model = svr_rbf.fit(xtrain,ytrain)
      kmodel = oc.fit(xtrain,ytrain)
      y_scores = kmodel.predict(xtest)
      print kmodel.score(xtest,ytest)
      eval_regres(ytest,y_scores)

EvalRUNwithSVM()
