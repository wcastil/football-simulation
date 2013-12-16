import random
import json
import learn
#import runningModel
import data_ops
with open('./data/rosters.txt') as rfile:
     rosters = json.load(rfile)
class Team:
    
    def __init__(self, name=None, fname=None, numgames=None, qbName=None ):
        
        self.team_name = name
        self.score = 0
        self.runModel = None
        self.n_neighbors = 5
        self.qbNames = map(str,rosters[name]['QB'])
        self.DEF_STATS = None
        self.PassData = data_ops.PassData('./data/2013_nfl_pbp_through_wk_12.csv')
        if fname is not None:
           #print "getting models with data: " + fname
           self.getRunModel(fname)
           self.learnFromPastGames(fname,numgames,self.qbNames)
           #self.knn = learn.learnKNN( self.allXdata, self.allYdata, n=5)
           self.knn = learn.learnKNN( self.teamRunningX, self.teamRunningY, n=5)
           ydata = []
           xdata = []
           for e in self.passplays:
               #get knn for completions only
               if e[-1] != 0:
                   xdata.append(e[0:-1])
                   ydata.append(e[-1])
           self.passKNN = learn.learnKNN( xdata, ydata,n=3) 
           #self.knn = learn.learnKNN(self.n_neighbors, self.teamRunningX, self.teamRunningY)
    def nextPlay(self, game, last_play, TIME):
        #sample from the real distrution later
        PLAY = [None, 0] 
        if last_play is not None:
            last_play = last_play[0]
        if game.scored == True:
           game.scored = False
           PLAY[0] = 'Kickoff' 
        elif last_play == 'Punt':
           PLAY[0] = 'PuntReturn'
        elif last_play == 'Kickoff':
           PLAY[0] = 'KickReturn'
        elif game.down < 4 and game.down > 0 or PLAY == None:
#            EVpass = (self.pass_value)*self.probOfCompletePass(game)
            EVpass = self.knn_pass_value(game)[0] *self.probOfCompletePass(game)
            EVrun = self.knn_run_value(game)[0]
            PLAY = max( [('Run',EVrun),('Pass',EVpass)], key=lambda e:e[1])
#            PLAY = random.choice(['Run', 'Pass']) 
        else:
            if game.yardline < 55:
               PLAY[0] = 'KickFieldGoal'
            else:
               PLAY[0] = 'Punt'

        return PLAY

    def learnFromPastGames(self, fname, numgames=None,qbName=None ):
            self.passplays = self.PassData.PassTrainData(teamname=self.team_name)
            #self.reader = learn.getReader(fname)
            #self.qbModel = learn.getQBModel(self.reader, self.team_name, self.qbNames, numgames)
            #self.passplays, self.qbOther = learn.getPassPlay(self.qbModel)
            self.completionModel = learn.getCompletionProbModel(self.passplays)
            total = 0.0
            num_success = 0
            for e in self.passplays:
                if e[-1] > 0:
                   num_success +=1
                   total += e[-1]
            self.pass_value = float(total)/len(self.passplays)

    def getRunModel(self, fname):
        R= data_ops.RunData(fname)
        self.DEF_STATS = R.getOppDefenseStats(self.team_name) 
        self.allXdata,self.allYdata = R.RunTrainData(fname)
#        self.teamRunningData = R.getRunPlays(data_ops.getReader(fname),self.team_name)
        self.teamRunningX, self.teamRunningY = R.RunTrainData(fname, self.team_name) 
#        self.teamRunningX = [e for e in self.teamRunningData]
 #       self.teamRunningY = [e.pop() for e in self.teamRunningX]

    def knn_pass_value(self, g):
        Xfeat = self.getPassFeatures(g)
        try:
            v = self.passKNN.predict(Xfeat)
        except:
            print "knn pass error"
            pass
        return v
    
    def knn_run_value(self, g):
        tms = self.getTimeFeaturesFromGame(g)
        scorediff = g.O.score - g.D.score
        eff, peff, reff = g.D.DEF_STATS
        Xfeat = tms+ [g.down,g.yards_to_first_down, g.yardline, scorediff,\
                      g.series_first_down, eff, reff]
        try:
            v = self.knn.predict(Xfeat)
        except:
            print "KNN error"
            pass
        return v



    def getTimeFeaturesFromGame(self, g): 
        t = g.time_left_this_game/60
        tms = []
        if g.quarter <= 2:
           tms+= [1,0]
        else:
           tms+= [0,1]
        if g.quarter == 2 and g.time_left_this_quarter < 180:
              tms.append(1)
        else:
              tms.append(0)
        if g.quarter == 4 and  g.time_left_this_quarter < 300:
             tms.append(1)
        else:
             tms.append(0)
        return tms

    def probOfCompletePass(self, g):
        Xfeat = self.getPassFeatures(g)
        prob_of_success = self.completionModel.predict_proba(Xfeat)[0][1]
        return prob_of_success

    def getPassFeatures(self, g):
        tms = self.getTimeFeaturesFromGame(g)
        scorediff = self.score - g.D.score
        eff, peff, reff = g.D.DEF_STATS
        Xfeat = tms+ [g.down,g.yards_to_first_down, g.yardline, scorediff,\
            g.series_first_down, eff,peff]
        return Xfeat
    



