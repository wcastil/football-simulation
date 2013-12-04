import pylab as pl
from sklearn.svm import SVR
import numpy as np
import learn
import team
from sklearn import linear_model
import re
import json
from sklearn import preprocessing
from sklearn import cross_validation
import runningModel

with open('rosters.txt') as rfile:
     rosters = json.load(rfile)

#def getTeamRunningModel(reader, teamname):
players = {}
run_re = 'up the middle|right guard|left guard|scrambles|right tackle|left tackle'
dir_re = '(middle)|(right)|(left)|(scrambles)' 
yard_re = 'for\s(-?[0-9]+)\syards'
player_re = '[A-Z].[A-Z]\w{2,27}'

def haveData(filename):
    try:
       with open(filename):
            return True
    except IOError:
       return False

class RunData():
      def __init__(self, fname):
          self.fname = fname
         
      def TrainData(self, fname=None, teamname=None):
          if fname is None:
             fname = self.fname
          Xall = []
          if teamname is  None:
             teams = [e[0:-1] for e in open('teams','r')]
          else:
             teams = [teamname]
          if not haveData('xtrainingset'):
            for tm in teams:
                tm = re.search('[A-Z]{2,3}',tm).group(0)
                Xall += self.getRunPlays(learn.getReader(fname), tm)
            
            with open('xtrainingset', 'w') as xtrainfile:
                 json.dump(list(Xall), xtrainfile)
          else:
            with open('xtrainingset', 'r') as xtrainfile:
                 Xall = json.load(xtrainfile)

          Xalltrain = [e[0:9] for e in Xall]
          Yalltrain = [e[-1] for e in Xall]
          return (Xalltrain,Yalltrain)



#Running features: [ IS_FIRST_HALF, IS_SECOND_HALF, close to half time, close to end game,\
#                     down, to first down, yd line, scorediff, series 1st downs, TARGET:  yards gaine]
      def getRunPlays(self,reader, teamname):
          f = []
          plays = []
          for row in reader:
              play = row[0].split(',')
              if teamname in play[0]:
                 d = play[11]
                 if self.isRunPlay(d, teamname):
                    f += [self.extractRunFeatures(play)]
                    #plays.append(f)
          return f
    
      def extractRunFeatures(self,p):
          timeLeft = learn.timeLeftFeatures(p[1:3])
          d = p[11]
          direction = self.getDirection(re.search(dir_re, d).group(0))
          yards = re.search(yard_re, d)
          if yards is not None:
             yards = yards.group(1)
          else:
             yards = 0.0
          player = re.search(player_re, d)
          # add player feature
          f = timeLeft+[float(e) for e in p[6:11]]+[float(yards)]
          return f
           
          
      
      def isRunPlay(self,d, teamname=None):
          player_name =  re.search(player_re, d) 
          if re.search(run_re, d) is not None and player_name is not None:  
                player_name = self.getPlayerName(d)
                if player_name is not None and teamname is not None:
                   if player_name in rosters[teamname]['RB'] or player_name in rosters[teamname]['QB']:
                      return True
                elif player_name is not None:
                     return True
          return False

      def getDirection(self,d):
          if d is None:
             return [0,0,0,0]
          elif d == 'middle':
             return [1,0,0,0] 
          elif d == 'right':
             return [0,1,0,0]
          elif d == 'left':
             return [0,0,1,0]
          elif d == 'scrambles':
             return [0,0,0,1]
    

    
      def getPlayerName(self,d):
          player_name = re.search(player_re, d)
          if player_name is not None:
             return player_name.group(0)
             player_name = player_name.group(0)
             pn = player_name[0]+'.'+player_name.split()[-1]
             return pn
          return None
