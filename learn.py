import game
import sys
import csv
import re
import numpy as np

games ={}
def get_play_from_row(row):
  elems = row[0].split("\t")
  return elems

def getReader(name):
    f = open(name, 'rU')
    reader = csv.reader(f, dialect=csv.excel_tab)
    return reader


# Methods for creating passing model and QB model 
#
#
def getQBModel(reader,name,QBname, NumGames=None):
#    name = 'CIN'
    if QBname is None:
      return None
    QBplays = []
    TEAMplays = []
    for row in reader: 
      play = row[0].split(',')  #get_play_from_row(row)
      if name in play[0]:
        if QBname in play[11]: 
           QBplays.append(play)
        else:
           TEAMplays.append(play)
    return QBplays
  
def getPassPlay(QBplays):
    PASSplays = []
    other = []
    for p in QBplays:
        if 'pass' in p[11] and 'TWO-POINT' not in p[11]:
            PASSplays.append( extractPassFeatures(p) )
        else:
            other.append(p)
    return (PASSplays,other)
#      if name in play[1]:
         
       
def extractPassFeatures(p): 
      print p
      if 'pass' in p[11] and 'TWO-POINT' not in p[11]:
        yards = re.search('for\s([0-9]+)\syards', p[11])
        timeLeft = timeLeftFeatures(p[1:3])
        if yards != None:
           y = yards.group(1)
           feats = timeLeft+p[6:11]+[y]
        else:
           feats = timeLeft+p[6:11]+[0]
      else:
          print p
          return None
      return [float(v) for v in feats]

def script():    
    reader = getReader('2013_nfl_pbp_through_wk_12.csv') 
    qb = getQBModel(reader, 'CIN', 'Dalton')
    passes,other = getPassPlay(qb)
    return passes

from sklearn import svm
def getCompletionProbModel(passplays):
  X = [e[0:-1] for e in passplays]
  Y = [-1 if e[-1] == 0 else 1 for e in passplays]
  m = svm.SVC(kernel='rbf', probability=True)
  m.fit(X,Y)
  return m

def getRunYardageModel(runplays):
    return 
  



def read_games(reader, numGames=-1):
    for row in reader:
        play = get_play_from_row(row)
        if play[1] not in games.keys():
            if numGames != -1 and len(games.keys()) > numGames:
                return
            this_game = play[1] 
            games[this_game] = [play]
        else:
           games[this_game].append(play)

def learnS():
  if len(sys.argv) < 2:
      print " must include filename"
  else:
      f = open(sys.argv[1], 'rU')
      reader = csv.reader(f, dialect=csv.excel_tab)
      labels = reader.next()[0].split('\t')
      read_games( reader , 2)
      print labels
      print games.keys()



#QB pass yardage
    
    
#Team run yardage


def timeLeftFeatures(p):
    halfs = []
    p = [int(e) for e in p]
    if int(p[0]) <= 2:  
       halfs += [1,0]
    else:
       halfs += [0,1]
    if p[0] == 2 and p[1] < 33:
          halfs.append(1)
    else:
          halfs.append(0)
    if p[0] == 4 and p[1] < 5: 
         halfs.append(1)
    else:
         halfs.append(0)
    return halfs



import numpy as np
import pylab as pl
from sklearn import neighbors
import testSet
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score

def learnKNN(n, xtrain, ytrain):
    n_neighbors = 5
    knc = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
    kmodel = knc.fit(xtrain,ytrain) 
    return kmodel
#y_scores = kmodel.predict(xtest)
#print y_scores
