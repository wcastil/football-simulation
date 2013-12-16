import game as SIM
import team
import plays
import sys


def sim_ATL_GB():
    W = "GB"
    L = "ATL"
def SimulateWeek14():
    match_ups = [['JAC','HOU'],['GB','ATL'],['TB','BUF'],['CIN','IND'],\
                  ['PHI','DET'],['KC','WAS'],['NYJ','OAK'],['MIA','PIT'],\
                  ['BAL','MIN'],['DEN','TEN'],['ARI','STL'],['SD','NYG'],\
                  ['SF','SEA'],['NO','CAR'],['CHI','DAL']]

    c = 0.0
    t = float(len(match_ups))
    for m in match_ups:
        W,L = m
        team_1 = team.Team(W, './data/2013_nfl_pbp_through_wk_12.csv', numgames=None)
        team_2 = team.Team(L,'./data/2013_nfl_pbp_through_wk_12.csv', numgames=None )
        res =simulate_games(team_1, team_2, num_games=100)
        if res[team_1.team_name] >= res[team_2.team_name]:
           print "Correct: " + W +" beats "+ L
           c+=1
    print str(float(c)/t) + " Correct"

    

#Rougly keep track of time and plays. Can make this more realistic after sim is running
PLAY_CLOCK = 40
AVG_PLAY = .75*PLAY_CLOCK+6 #36 seconds
SECONDS_PER_QUARTER = 900

def switchOffense(g):
    tmp = g.O
    g.O = g.D
    g.D = tmp

def simulate_games(team_1, team_2,num_games=100, verbose=False):
    team_1_wins = 0
    team_2_wins = 0
    team_wins = {team_1.team_name:0, team_2.team_name:0}
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

    print ""
    print team_wins
    return team_wins

#simulate_games(team_1,team_2)
#SimulateWeek14()

print "Simulating DEN vs SD, Real outcome was SD winning"
team_1 = team.Team('DEN', './data/2013_nfl_pbp_through_wk_12.csv', numgames=None)
team_2 = team.Team('SD','./data/2013_nfl_pbp_through_wk_12.csv', numgames=None )
simulate_games(team_1, team_2,num_games=10, verbose=False)

#SimulateWeek14()
