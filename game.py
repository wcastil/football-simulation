"""
"""
import copy
import os
import random
import time
import team
import plays

       
PlayDict = plays.PlayDict    


class Game:

    def __init__(self,team_1=None, team_2=None, 
                  classifiers=None):
        
        self.team_1 = None
        self.team_2 = None
        self.game_classifiers = classifiers
        score = {}
        score[self.team_1] = 0
        score[self.team_2] = 0
        self.score = score 
        self.game_stats = {}
        self.yards_to_first_down = 10
        self.yards_to_toucdown = 80
        self.yardline = 80
        self.down = 1
        self.O = None
        self.D = None
        self.series_first_down = 0
        self.time_left_this_quarter = 900
        self.time_left_this_game = 4*900
        self. quarter = 1
        self.winner = None
        self.switchOffense = False
        self.turn_over_on_downs = False
        self.scored = False
        self.summary = []
    
    def isEndState(self,TIME):
        if self.quarter > 4:# and self.time_left_this_quarter <= 0:
           if self.O.score > self.D.score:
              self.winner = self.O
           elif self.O.score < self.D.score:
              self.winner = self.D
           else:
              self.winner = 'TIE'
           print self.winner 
           print self.O.score, self.D.score
           return True
        else:
           return False
        
    def executePlay(self,PLAY, TIME):
        # random.seed()
        #time.sleep(0.3)
        # only the offense runs plays right now
        #determine the success of the play
        #determine which players were involved
        #determine defense and environment reponse/result and update game state
        result = PlayDict[PLAY](self) 
         
        s =self.O.team_name+": Down: " +str(self.down)\
            + ", BALL ON: "+str(self.yardline)\
            +", PLAY: "+str(PLAY)\
            +"-"+str(result) + " yards gained"
        self.summary.append(s)

        self.updateState(PLAY, result)

        self.updateTime(result, PLAY)
        return self.isEndState(TIME)
 

    def updateState(self, PLAY, result):
        if PLAY == 'KickFieldGoal':
           if result  == True: #made field goal
              self.summary[-1] +=(" 3 points scored ")
              self.series_first_down = 0
              self.O.score += 3
              self.scored = True

           else:
              self.turn_over_on_downs = True
              self.series_first_down = 0
              self.switchOffense = True
              self.down = 1
              if self.yardline == 0:
                 self.yardline = 100
              else:
                 self.yardline = 100 - self.yardline 
        elif PLAY == 'Kickoff':
             self.summary.append(self.O.team_name+" Kicked off")
             self.down = 0
             self.switchOffense = True
             self.yardline = 100
        elif PLAY == 'Punt':
             self.summary.append(self.O.team_name+" Punted.")
             self.down += 1
             self.switchOffense = True
             self.yardline = 100
        elif PLAY == 'Pass' or PLAY == 'Run': 
              if self.TouchDown(result, PLAY):
                 self.summary[-1]+=(" 7 points scored ")
                 self.O.score += 7
                 self.scored = True
                 #self.switchOffense = True
                 self.down = 0
                 self.yardline = 100
              else:
                  self.updateDrive(result, PLAY)
        elif PLAY == 'KickReturn':
             self.summary.append(self.O.team_name+" Returned kick for "+str(result))
             self.updateYardline(result)
             self.down = 1
        elif PLAY == 'PuntReturn':
             self.summary.append(self.O.team_name+" Returned punt for "+str(result))
             self.updateYardline(result)
             self.down = 1
              

    def updateTime(self, result, PLAY):
        #estimate each play takes 30 seconds off the clock for now
        if PLAY in ['Kickoff','KickReturn']: 
           return
        self.time_left_this_quarter -= 30
        self.time_left_this_game -= 30
        if self.time_left_this_quarter <= 0:
           print self.quarter
           self.time_left_this_quarter = 900
           self.quarter +=1


    def TouchDown(self, result, PLAY):
        y = self.yardline
        if y >= 0 and y-result < 0:
           return True
        return False
        
    
    def updateDrive(self, result, PLAY):
           self.down += 1
           if self.down > 4 and (result <= 0 or self.yards_to_first_down - result > 0):
              self.switchOffense = True
              self.turn_over_on_downs = True
              self.series_first_down = 0
              self.down = 1
              if self.yardline == 0:
                 self.yardline = 100
              else:
                 self.yardline = 100 - self.yardline
              self.summary[-1] += ", Turned over on downs "
           elif self.yards_to_first_down - result <= 0:
              self.summary[-1] += ", First Down reached, "
              self.down = 1
              self.series_first_down = 1
              self.yards_to_first_down = 10
              self.updateYardline(result)
              self.summary[-1] += "[Yardline: "+str(self.yardline)+" Result: "+str(result)+", YTF:"+str(self.yards_to_first_down)+ " ]"
           else:
                 self.yards_to_first_down -= result
                 self.updateYardline(result)
                 self.summary[-1] += "[Yardline: "+str(self.yardline)+" Result: "+str(result)+", YTF:"+str(self.yards_to_first_down)+ " ]"
           
    def updateYardline(self, result):
       self.yardline -= result
     

#check for safety

              

        
        




    def new_game(self):
        """
        reset the game state for a new match
        """
