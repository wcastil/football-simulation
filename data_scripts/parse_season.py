import csv
import sys

if len(sys.argv) < 2:
   print "Must include filename arg"
   exit()
f = open(sys.argv[1], 'rU')
reader = csv.reader(f, dialect=csv.excel_tab)

games = {}

def get_play_from_row(row):
  elems = row[0].split("\t")
  return elems


def read_games(reader):
    for row in reader:
        play = get_play_from_row(row)
        if play[1] not in games.keys():
           this_game = play[1] 
           games[this_game] = [play]
        else:
           games[this_game].append(play)



#read_games(reader)


           
        
        

