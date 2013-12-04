import re
import json
import learn
import trainSet

with open('rosters.txt') as rfile:
     rosters = json.load(rfile)

#def getTeamRunningModel(reader, teamname):
players = {}
run_re = 'up the middle|right guard|left guard|scrambles|right tackle|left tackle'
dir_re = '(middle)|(right)|(left)|(scrambles)' 
yard_re = 'for\s(-?[0-9]+)\syards'
player_re = '[A-Z].[A-Z]\w{2,27}'

class runningModel:
      def __init__(self, teamname=None, fname=None, numgames=None):

          self.teamname = teamname 
          self.fname = fname
          if fname is not None:
              new_reader = learn.getReader(fname)
              self.runplays = self.getRunPlays(new_reader, teamname)

          self.allrunplays = trainSet.TrainData(fname)


#Running features: [ IS_FIRST_HALF, IS_SECOND_HALF, close to half time, close to end game,\
#                     down, to first down, yd line, scorediff, series 1st downs, TARGET:  yards gaine]
      def getRunPlays(self, reader, teamname):
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
