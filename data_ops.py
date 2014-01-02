import pylab as pl
from sklearn.svm import SVR
import numpy as np
import learn
import team
from sklearn import linear_model
import re
import json
import csv
from sklearn import preprocessing
from sklearn import cross_validation
import dstats
#import runningModel

with open('./data/rosters.txt') as rfile:
     rosters = json.load(rfile)


def haveData(filename):
    try:
       with open(filename):
            return True
    except IOError:
       return False

class FootballData():
      def __init__(self, fname):
          self.fname = fname
      
      def getOppDefenseStats(self, opp):
          eff, pass_eff, rush_eff = dstats.DEF_STATS[opp]
          eff = 1-(eff+.50)
          rush_eff = 1-(rush_eff+.50)
          pass_eff = 1-(pass_eff+.50)
          return [eff, pass_eff,rush_eff]
      
      def getPlayerName(self,d):
          player_name = re.search(player_re, d)
          if player_name is not None:
             return player_name.group(0)
             player_name = player_name.group(0)
             pn = player_name[0]+'.'+player_name.split()[-1]
             return pn
          return None


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

      def timeLeftFeatures(self,p):
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

class RunData(FootballData):
         
      def RunTrainData(self, fname=None, teamname=None):
          if fname is None:
             fname = self.fname
          Xall = []
          if teamname is  None:
             outfilename = './data/allTrainData'
             teams = [e[0:-1] for e in open('./data/teams','r')]
          else:
             outfilename = './data/'+teamname+'_runTrain'
             teams = [teamname]
          if not haveData(outfilename):
            for tm in teams:
                tm = re.search('[A-Z]{2,3}',tm).group(0)
                Xall += self.getRunPlays(getReader(fname), tm)
            
            StoreAsJSON(outfilename, Xall)
          else:
            Xall = GetFromJSON(outfilename)

          Yalltrain = [e.pop() for e in Xall]
          Xalltrain = Xall
          return (Xalltrain,Yalltrain)


#Running features: [ IS_FIRST_HALF, IS_SECOND_HALF, close to half time, close to end game,\
#                     down, to first down, yd line, scorediff, series 1st downs, TARGET:  yards gaine]
# and now defense effciency and  run defense effciency
      def getRunPlays(self,reader, teamname):
          f = []
          plays = []
          for row in reader:
              play = row[0].split(',')
              if teamname in play[4]:
                 d = play[11]
                 if self.isRunPlay(d, teamname):
                    f += [self.extractRunFeatures(play)]
                    #plays.append(f)
          return f
    
      def extractRunFeatures(self,p):
          timeLeft = self.timeLeftFeatures(p[1:3])
          d = p[11]
          direction = self.getDirection(d)
          yards = re.search(yard_re, d)
          if yards is not None:
             yards = yards.group(1)
          else:
             yards = 0.0
          opp = p[5]
          #player = re.search(player_re, d)
          # add player feature
          eff, peff, reff = self.getOppDefenseStats(opp)
          f = timeLeft+[float(e) for e in p[6:11]]+[eff,reff]+[float(yards)]
          return f
           

      def getDirection(self,des):
          d = re.search(dir_re, des).group(0)
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
    

    


#-- Define Passing Data Class -- #
class PassData(FootballData):

      def PassTrainData(self, fname=None, teamname=None):
          outfilename = "./data/passTrainData"
          if fname is None: fname = self.fname
          Xall = []
          if teamname is None:
             teams = [e[0:-1] for e in open('./data/teams','r')]
          else:
             outfilename = './data/'+teamname+'_passTrain'
             teams = [teamname]

          if not haveData(outfilename):
             for tm in teams:
                 tm = re.search('[A-Z]{2,3}',tm).group(0)
                 QBs = map(str,rosters[tm]['QB'])
                 Xall += self.getPassPlays(getReader(fname), tm, QBs, 'R.Gronkowski')
             StoreAsJSON(outfilename, Xall)
          else:
             Xall = GetFromJSON(outfilename)
          return Xall 

          
      def getPassPlays(self, r, tm, QBs, remove_players=None):
          QBplays = [] 
          OtherPlays = []
          for row in r:
              play = row[0].split(',')  
              if tm in play[4]: #if it is the correct team on offense
#                 for qb in QBname:
                  #doing this for team passing right now
                  if 'pass' in play[11] and 'TWO-POINT' not in play[11]:
                      if remove_players is not None:
                         if remove_players not in play[11]:
                             QBplays.append(self.extractPassFeatures(play))
                  else:
                      OtherPlays.append(play)
          return QBplays

      def extractPassFeatures(self,p): 
            if 'pass' in p[11] and 'TWO-POINT' not in p[11]:
              yards = re.search('for\s([0-9]+)\syards', p[11])
              timeLeft = self.timeLeftFeatures(p[1:3])
              eff, peff, reff = self.getOppDefenseStats(p[5])
              if yards != None:
                 y = yards.group(1)
                 feats = timeLeft+p[6:11]+[eff,peff]+[y]
              else:
                 feats = timeLeft+p[6:11]+[eff,peff]+[0]
            else:
                return None
            return [float(v) for v in feats]





#---General data helper methods ---#
def get_play_from_row(row):
  elems = row[0].split("\t")
  return elems

def StoreAsJSON(outname,data):
    with open(outname,'w') as xfile:
         json.dump(list(data),xfile)

def GetFromJSON(outfilename):
    with open(outfilename, 'r') as xfile:
         return json.load(xfile)


def getReader(name):
    f = open(name, 'rU')
    reader = csv.reader(f, dialect=csv.excel_tab)
    return reader

#-- Regular expressions -- #
run_re = 'up the middle|right guard|left guard|scrambles|right tackle|left tackle'
dir_re = '(middle)|(right)|(left)|(scrambles)' 
yard_re = 'for\s(-?[0-9]+)\syards'
player_re = '[A-Z].[A-Z]\w{2,27}'
