football-simulation
===================
Code requires scikit library and python 2.7

Quick summary:
Simulate.py has the code for specifying the simulation,prints number of games won by each team
Game simulation is in game.py
Agent=Team class in team.py
data_ops.py handles the parsing and retrieving of training data
learn.py has the methods for completion probabilty and training a KNN model.
plays.py has method of executing a play, although this is only used by the environment, team.py has play methods for agents

Testing:
regression_testing.py has the framework that was used to test rushing regression
pass_regression_testing.p has the same but for passing
knn.py has the code used for testing KNN algorithms and SVMs
SVM_testing has the orginal code for testing SVMs
hmm.py has some messing around with HMM's


Data files.
dstats.py is used for loading defensive team data.
data/ directory stores the parsed training data and other data files
data_scripts/ has the files used for scraping data and parsing

The simulation code is in game.py and team.py. Each team/agent is part of the Team class in team.py,
and this is where the decision by an agent to choose a play is made.

