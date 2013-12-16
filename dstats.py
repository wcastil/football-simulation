#DEF rating, PASS rating, RUSH rating
import re
from bs4 import BeautifulSoup, SoupStrainer

f = open('./data/teamdef', 'r+')

DEF_STATS = {}
soup = BeautifulSoup(f)


team_rosters={}

for tr in soup.find_all('tr'):
    TD = [] 
    for td in tr:
        TD.append(td)

    nm = str(TD[3].getText())
    DEF_STATS[nm] = (float(TD[5].getText()[0:-1])/100, float(TD[13].getText()[0:-1])/100,\
        float(TD[17].getText()[0:-1])/100)

print "Defensive Stats Loaded"




