# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:24:07 2020

@author: edunu
"""

import requests
from bs4 import BeautifulSoup
import re


grupos = ("Current teams", "Classic teams", "All-Time teams",
          "All-Decade teams", "All-Star Teams")

# GENERATE TUPLE OF ALL TEAMS
teams = []
for group in grupos:
    url = "https://www.2kratings.com/" + group.lower().replace(" ", "-")
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    fn = BeautifulSoup(str(soup.find_all("tr"))).text
    fn = fn.split(",   ")
    
    for _ in range(1,len(fn)):
        tm = re.search('([-\w\s]+)\s[T\-\d]{20}', fn[_])
        teams.append(tm.group(1))

for _ in range(135, len(teams)):
    teams[_] = "2019-20 " + teams[_]
    if _ in [135, 136]:
         teams[_] = teams[_] + " All-Stars"
         
# COLUMN NAMES
db = {}
db["player"] = []

url = "https://www.2kratings.com/lebron-james"
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

col = []

dat = soup.find_all("div", class_="header-subtitle")
dat = BeautifulSoup(str(BeautifulSoup(str(dat)).find_all("p")[2:])).text.replace("[","").replace("]", "")
datc = re.split(',\s|\s\|\s', dat)


subt = soup.find_all("li", class_ = "mb-1")
tit = soup.find_all("div", class_="card-header")

for i in range(9):
    atr = re.search('([^:]+):\s+([\w#].+)', datc[i])
    col.append(atr.group(1))
    
col = ["Overall"] + col[0:3] + ["Position1", "Position2"] + col[4:] + ["Rank current", "Rank all"]
    
for i in range(len(col)):
    db[col[i]] = []

for _ in range(2,11):
    atr = BeautifulSoup(str(tit[_])).text
    atr = re.search('^(\d+)\s+(\D+)', atr)
    db[atr.group(2)] = []
    
for _ in range(0,36):
    atr = BeautifulSoup(str(subt[_])).text
    atr = re.search('^(\d+)\s+(\D+)', atr)
    db[atr.group(2)] = []

db["Team_Category"] = []

for j in range(5):
    print("\n### " + teams[j] + "\n" + str(j + 1) + " of " + str(len(teams)) + "\n")
    players = []
    
    team = teams[j].lower().replace(" ", "-")
    url = "https://www.2kratings.com/teams/" + team
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    names = BeautifulSoup(str(soup.find_all("div", "table-responsive h-100 overflow-hidden")))
    names = names.find_all("span", class_="entry-font")
    
    for _ in range(len(names)):
        players.append(BeautifulSoup(str(names[_])).text)
        
    for i in range(len(players)):
        low = players[i].lower().replace("’", "").replace(".", "").replace(" ", "-")
        if low in ["jacob-evans-iii", "kevin-knox-ii",
                   "melvin-frazier-jr", "harry-giles-iii"]:
            low = low.replace("-iii", "").replace("-ii", "").replace("-jr", "")
        if j > 29 and j < 135:
            low = low + "-" + team
            if j in range(127, 133):
                low = low[:-10]
        if players[i] == "Bobby Jones (Robert Clyde)":
            low = "bobby-jones-" + team
        url = "https://www.2kratings.com/" + low
        if url == "https://www.2kratings.com/landry-fields-2011-12-new-york-knicks":
            break
        if url == "https://www.2kratings.com/lebron-james-2012-13-miami-heat":
            url = "https://www.2kratings.com/lebron-james-12-13-miami-heat"
        page = requests.get(url)
        
        soup = BeautifulSoup(page.text, "html.parser")
        
        oval = BeautifulSoup(str(soup.find_all("div", class_= "text-center"))).text
        oval = oval.split(", ")
        try:
            db["Overall"].append(int(oval[7]))
        except:
            continue
        
        db["player"].append(players[i])
        dat = soup.find_all("div", class_="header-subtitle")
        dat = BeautifulSoup(str(BeautifulSoup(str(dat)).find_all("p")[2:])).text.replace("[","").replace("]", "")
        dat = re.split('\s?,\s|\s\|\s', dat)
        if "Position:" in dat[2]:
            dat = dat[0:2] + [""] + dat[2:]
        if "Jersey" in dat[5]:
            dat = dat[0:5] + [""] + dat[5:]
        if "Jersey" not in dat[6]:
            dat = dat[0:6] + [""] + dat[6:]
        if "Year" not in dat[7]:
            dat = dat[0:7] + [""] + dat[7:]
        if "Ranks #" in dat[8]:
            dat = dat[0:8] + [""] + dat[8:]
        if "Ranks #" not in dat[9]:
            dat = dat[0:9] + dat[10:]
        for n in range(11):
            if n in [0,1]:
                se = re.search(':\s+([\w].+)', dat[n])
                db[col[n+1]].append(se.group(1))
            elif n == 2:
                if dat[2] != "":
                    se = re.search(':\s+([\w].+)', dat[n])
                    db[col[n+1]].append(se.group(1))
                else:
                    db[col[n+1]].append("-")
            elif n == 3:
                if "/" in dat[n]:
                    se = re.search(':\s(\w+)\W+(\w+)', dat[n])
                    db[col[n + 1]].append(se.group(1))
                    db[col[n + 2]].append(se.group(2))
                else:
                    se = re.search(':\s(\w+)', dat[n])
                    db[col[n + 1]].append(se.group(1))
                    db[col[n + 2]].append("-")
            elif n == 4:
                se = re.search(':.+\((\d+)', dat[n])
                db[col[n+2]].append(int(se.group(1)))
            elif n == 5:
                if dat[5] != "":
                    se = re.search(':.+\((\d+)', dat[n])
                    db[col[n+2]].append(int(se.group(1)))
                else:
                    db[col[n+2]].append(0)            
            elif n == 6:
                if dat[6] != "":
                    se = re.search(':\s+#([\w].?)', dat[n])
                    db[col[n+2]].append(int(se.group(1)))
                else:
                    db[col[n+2]].append(100)
                
            elif n == 7:
                if dat[7] != "":
                    se = re.search(':.+(\d+)', dat[n])
                    db[col[n+2]].append(int(se.group(1)))
                else:
                    db[col[n+2]].append(0)
            elif n == 8:
                if dat[8] != "": 
                    se = re.search(':\s+([\w].+)', dat[n])
                    db[col[n+2]].append(se.group(1))
                else:
                    db[col[n+2]].append("-")
            elif n in [9, 10]:
                se = re.search('#(\d+)', dat[n])
                db[col[n+2]].append(int(se.group(1)))
        
        subt = soup.find_all("li", class_ = "mb-1")
        tit = soup.find_all("div", class_="card-header")
        
        for _ in range(2,11):
            atr = BeautifulSoup(str(tit[_])).text
            atr = re.search('^(\d+)\s+(\D+)', atr)
            db[atr.group(2)].append(int(atr.group(1)))
        

        for m in range(0,36):
                atr = BeautifulSoup(str(subt[m])).text
                atrb = re.search("^\s?(\d+)\]?'?\s+(\D+)", atr)
                if atr[0] == "-":
                    atrb = re.search("[\-]\s+(\D+)", atr)
                    db[atrb.group(1)].append(0)
                    continue
                db[atrb.group(2)].append(int(atrb.group(1)))
        if j > 132:
            db["Team"][-1] = teams[j]
        if j < 30:
            db["Team_Category"].append("Current")
        elif j < 97:
            db["Team_Category"].append("Classic")
        elif j < 133:
            db["Team_Category"].append("All-Time")
        elif j >= 133:
            db["Team_Category"].append("All-Star")
        print(players[i])
        
        
import pandas as pd

dosca = pd.DataFrame(db) 

dosca.to_csv("nba2k20.csv", index = False)
