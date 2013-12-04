import random
import learn
import runningModel
import trainSet

class Team:
    
    def __init__(self, name=None, fname=None, numgames=None, qbName=None ):
        
        self.team_name = name
        self.score = 0
        self.runModel = None
        self.n_neighbors = 5
        if fname is not None:
           self.getRunModel(fname)
           self.learnFromPastGames(fname,numgames,qbName)
           self.knn = learn.learnKNN(self.n_neighbors, self.allXdata, self.allYdata)
    def nextPlay(self, game, last_play, TIME):
        #sample from the real distrution later
        PLAY = None
        if game.scored == True:
           game.scored = False
           PLAY = 'Kickoff' 
        elif last_play == 'Punt':
           PLAY = 'PuntReturn'
        elif last_play == 'Kickoff':
           return 'KickReturn'
        elif game.down < 4:
            EVpass = (self.pass_value)*self.probOfCompletePass(game)
            EVrun = self.knn_run_value(game)
            #print EVpass, EVrun
            PLAY = max( [('Run',EVrun),('Pass',EVpass)], key=lambda e:e[1])[0]

#            PLAY = random.choice(['Run', 'Pass']) 
        else:
            if game.yardline >= 0 and game.yardline <= 40:
               PLAY = 'KickFieldGoal'
            elif game.yardline < 0 or game.yardline > 40:
               PLAY = 'Punt'
        return PLAY

    def learnFromPastGames(self, fname, numgames=None,qbName=None ):
        if qbName is not None:
            if qbName != None:
               self.qbName = qbName
            self.reader = learn.getReader(fname)
            if numgames == None:
               self.qbModel = learn.getQBModel(self.reader, self.team_name, self.qbName, numgames)
            self.passplays, self.qbOther = learn.getPassPlay(self.qbModel)
            self.completionModel = learn.getCompletionProbModel(self.passplays)
            total = 0.0
            num_success = 0
            for e in self.passplays:
                if e[-1] > 0:
                   num_success +=1
                   total += e[-1]
            self.pass_value = float(total)/len(self.passplays)

    def getRunModel(self, fname):
        R= trainSet.RunData(fname)
        self.allXdata,self.allYdata = R.TrainData(fname,self.team_name)
        self.teamRunningData = R.getRunPlays(learn.getReader(fname),self.team_name)

    
    def knn_run_value(self, g):
        tms = self.getTimeFeaturesFromGame(g)
        scorediff = self.score - g.D.score
        Xfeat = tms+ [g.down,g.yards_to_first_down, g.yardline, scorediff,\
                      g.series_first_down]
#        print Xfeat
        v = self.knn.predict(Xfeat)
#        print v
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
        tms = self.getTimeFeaturesFromGame(g)
        scorediff = self.score - g.D.score
        Xfeat = tms+ [g.down,g.yards_to_first_down, g.yardline, scorediff, g.series_first_down]
        #print Xfeat

        prob_of_success = self.completionModel.predict_proba(Xfeat)[0][1]
        return prob_of_success
    



