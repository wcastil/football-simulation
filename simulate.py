import game as SIM
import team
import plays

t1 = 'NO'
t2 = 'SEA'
q1 = 'Brees'
q2 = 'Wilson'
team_1 = team.Team(t1, '2013_nfl_pbp_through_wk_12.csv', numgames=None, qbName=q1)
team_2 = team.Team(t2,'2013_nfl_pbp_through_wk_12.csv', numgames=None, qbName=q2)

#Rougly keep track of time and plays. Can make this more realistic after sim is running
PLAY_CLOCK = 40
AVG_PLAY = .75*PLAY_CLOCK+6 #36 seconds
SECONDS_PER_QUARTER = 900

def switchOffense(g):
    tmp = g.O
    g.O = g.D
    g.D = tmp

team_1_wins = 0
team_2_wins = 0
team_wins = {team_1.team_name:0, team_2.team_name:0}
#Create the Game simulation with the 2 teams
for i in range(0, 100):
    g = SIM.Game(team_1, team_2)


    g.O,g.D = plays.FlipCoin(team_1,team_2)
#j    print "Offense is: " + str(g.O.team_name)
 #   print "Defense is: " + str(g.D.team_name)



    last_play = None
    next_play = None
    TIME = g.time_left_this_quarter
    while True:
#    if g.switchOffense:
     #      switchOffense(g)
      #     g.switchOffense = False

        last_play = next_play
        next_play = g.O.nextPlay(g,last_play, TIME)
        #if last_play in ['KickOff', 'Punt'] or g.turn_over_on_downs or g.scored:
        if g.switchOffense: 
           g.turn_over_on_downs = False
           g.scored = False
           g.switchOffense = False
#       g.down = 1
           g.summary.append("Switched Offense")
           #print "SWITCHED OFFENSE"
           switchOffense(g)
           
        if g.executePlay(next_play, TIME): 
#           for s in g.summary:
#               print s
           #print g.O.team_name+" "+str(g.O.score)
           #print g.D.team_name+" "+str(g.D.score)
           if g.O.score > g.D.score:
              team_wins[g.O.team_name]+=1
           else:
              team_wins[g.D.team_name]+=1
           #game is over
           break
           
        

    print "End of game: "

print team_wins
#print game stats

#Update team state?



#set agent on offense
#set agent defense

#decide which play, based on expected return and some amount of randmoness or risk
#type of defensive play?

#if run play, determine yardage
#if pass play, determine pass yardage
#update game state, next play


