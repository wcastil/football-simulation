from bs4 import BeautifulSoup, SoupStrainer
import urllib2
from mechanize import Browser
import re


br = Browser()
hm =br.open('http://www.footballdb.com/teams')
soup = BeautifulSoup(urllib2.urlopen(hm.geturl()).read())
f = re.compile(r'/teams/nfl/\w+-\w{0,15}/roster|\w+-\w+-\w+/roster')

team_rosters={}

links = br.links(url_regex=f)
lnk_list = [l for l in links]



count =0 
for link in lnk_list:
    print count
    count +=1
    if count > 32:
       break
    teamname =link.attrs[0][1].split('/')[3]
    roster = {}
    br.follow_link(link)
    print br.title()
    #s = BeautifulSoup(urllib2.urlopen(br.geturl()).read())
    s = BeautifulSoup(urllib2.urlopen(br.geturl()).read(),parse_only=SoupStrainer('tr',{'class':'row1'}))
    s2 = BeautifulSoup(urllib2.urlopen(br.geturl()).read(),parse_only=SoupStrainer('tr',{'class':'row0'}))
    soups = [s,s2]
    pos_re = re.compile('[A-Z][A-Z]|P$|K$|C$')
    pname = re.compile('[A-Z][a-z]+\s[A-Z][a-z]+')
    for soup in soups:
      for tr in soup.find_all('tr'):
          pos = tr.find('td', text= pos_re) 
          if pos:
             fullname = tr.find('td',text=pname)
             if fullname:
                 fullname = fullname.getText()
                 pos = pos.getText()
                 name = fullname[0]+"."+fullname.split()[1] 
                 if pos in roster.keys():
                    roster[pos] += [name]
                 else:
                    roster[pos] = [name]
                 roster[name]=pos
             
    team_rosters[teamname]=roster

#print team_rosters.keys()
import json
with open('rosters.txt','w') as outfile:
     json.dump(team_rosters,outfile)



          

