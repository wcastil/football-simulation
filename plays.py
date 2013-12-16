import random

random.seed()
def flip(p):
    return False if random.random() < p else True

def FlipCoin(team_1,team_2):
    O = random.choice([team_1,team_2])
    if O == team_1:
      return (team_1, team_2)
    else:
      return (team_2, team_1)

def running_play(game):    
    #update this with dist
    gain = game.O.knn_run_value(game)
    return gain
    #jgains = [0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,9,10,10,11,11,12,12,13,14,15]
    #return random.choice(gains)
    
def pass_play(game):
    gains = [0]*7+[2]*5+[3,4]*4+[5]*3+[6,7,8]*2+[9,10,11]*2+[12,13,14,15,16,17,18,19,20,22,24,25]
    return random.choice(gains)

def kick_off(game):
    return 0

def field_goal_attempt(game):
    y = game.yardline
    if y > 0 and y <= 15: 
       return flip(0.05)
    if y > 15 and y <= 25:
       return flip(0.09)
    if y > 25 and y <= 38:
       return flip(0.20)
    if y > 38 and y <= 44:
       return flip(0.30)
    if y > 44 and y <= 49:
       return flip(0.35)
    if y == 50 or y < -40:
       return flip(0.70)
    if y <= -1 and y > -40:
       return False

def kick_return(game):
    #add distribution over returns
    gains = [20]*5+[25]*4+[30]*3+[40]*2 
    #return the yardline of the ball after the kick
    return random.choice(gains)

def punt_return(game):
    #add distribution over returns
    gains = [0,1,2,3,4,5,6,7]*3+[20]*4+[8,9,10,11,12,13,14,15,16,17,18,19]*2+[25,30,35,40,45,50,55,60,65] 
    #return the yardline of the ball after the kick
    return random.choice(gains)


PlayDict = {}
PlayDict['Run'] = running_play 
PlayDict['Pass'] = pass_play
PlayDict['KickFieldGoal'] = field_goal_attempt
PlayDict['KickReturn'] = kick_return
PlayDict['PuntReturn'] = punt_return
PlayDict['Punt'] = lambda x: 0
PlayDict['Neel'] = 0 #change to have function affect the game clock
PlayDict['Kickoff'] = kick_off
