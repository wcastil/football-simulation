import game as SIM
import team
import plays
import sys, getopt
import json



def simulate_week(wkNum, numGames, already_played=True, inc="",cor=""):
    with open('./data/week'+str(wkNum), 'r+') as ifile:
         matches = json.load(ifile)
         matches = map(str,matches)


    c = 0.0
    t = float(len(matches))/2
    i = 0
    while i < range(len(matches)):
        if i >= 31:
          break
    
        W = str(matches[i])
        L = str(matches[i+1])
        if W=='WSH':
           W='WAS'
        elif L=='WSH':
           L='WAS'
        team_1 = team.Team(W, './data/2013_nfl_pbp_through_wk_12.csv', numgames=None)
        team_2 = team.Team(L,'./data/2013_nfl_pbp_through_wk_12.csv', numgames=None )
        res =simulate_games(team_1, team_2, num_games=numGames)
        if already_played:
           inc = "Incorrect: "
           cor = "Correct: "
        if res[team_1.team_name] >= res[team_2.team_name]:
           print cor + W +" beats "+ L +" "+str(100*team_wins[W]/float(numGames)) +" percent of the time"
        else:
           print inc + L +" beats "+ W +" "+str(100*team_wins[L]/float(numGames)) +" percent of the time" 
           

           c+=1
        i=i+2
    if len(cor) > 1:
      print str(float(t-c)/t) + " Correct"

    

#Rougly keep track of time and plays. Can make this more realistic after sim is running
PLAY_CLOCK = 40
AVG_PLAY = .75*PLAY_CLOCK+6 #36 seconds
SECONDS_PER_QUARTER = 900

def switchOffense(g):
    tmp = g.O
    g.O = g.D
    g.D = tmp

team_wins = {}
def simulate_games(team_1, team_2,num_games=100, verbose=False):
    team_1_wins = 0
    team_2_wins = 0
#    team_wins = {team_1.team_name:0, team_2.team_name:0}
    team_wins[team_1.team_name] = 0
    team_wins[team_2.team_name] = 0
    for i in range(0, num_games):
        team_1.score = 0
        team_2.score = 0
        g = SIM.Game(team_1, team_2)
        g.O,g.D = plays.FlipCoin(team_1,team_2)
        if verbose==True:
            print "Offense is: " + str(g.O.team_name)
            print "Defense is: " + str(g.D.team_name)

        last_play = None
        next_play = None
        TIME = g.time_left_this_quarter
        while True:
            last_play = next_play
            next_play = g.O.nextPlay(g,last_play, TIME)
            if g.switchOffense: 
               g.turn_over_on_downs = False
               g.scored = False
               g.switchOffense = False
               g.summary.append("Switched Offense")
               if verbose==True:
                  print "SWITCHED OFFENSE"
               switchOffense(g)
               
            if g.executePlay(next_play, TIME): 
               if g.O.score > g.D.score:
                  team_wins[g.O.team_name]+=1
               else:
                  if verbose:
                     for s in g.summary:
                         print s
                  team_wins[g.D.team_name]+=1
               #game is over
               break
               

#        print g.O.team_name+" "+str(g.O.score)
 #       print g.D.team_name+" "+str(g.D.score)
        sys.stdout.write(".")    
        sys.stdout.flush()
        if verbose:
            print "End of game: "

    return team_wins




def main(argv):
    wkNum = -1
    numGames = 10
    already_played = True
    try:
      opts, args = getopt.getopt(argv,"w:g:p",["week=","numgames="])
    except getopt.GetoptError:
       print 'simulate.py -w for week, -g for number of games\n or -h for home team and -a for away team'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-w':
          wkNum = arg
          print wkNum
       elif opt in '-g':
          numGames = arg
       elif opt in '-p':
          already_played = False
       else:
         sys.exit(2)
    if wkNum != -1:
       print "Simulating Week: " + str(wkNum) +" with "+str(numGames)+" games per matchup"
       simulate_week(int(wkNum),int(numGames), already_played) 

if __name__ == "__main__":
   main(sys.argv[1:])
