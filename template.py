import csv, itertools, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

file_path = "/Users/nchen26/kitchen/BlueChips-Algorithms/NSL_Regular_Season_Data.csv"

with open(file_path, newline='') as rsrd:
    reader = csv.reader(rsrd)
    rsd = list(reader)

# OOP
names = rsd.pop(0)
class team:
    def __init__(self, score=0, mpa=0, mph=0, tg=0, tgaa=0, tgah=0, tp=0, txg=0, mp=0, shots=0, tgc=0, shotsc=0, corners=0):
        self.score = score 
        self.mpa = mpa # match played away
        self.mph = mph # match played home
        self.tg = tg # total goals
        self.tgaa = tgaa 
        self.tgah = tgah
        self.tp = tp # total possession
        self.txg = txg # total xG
        self.mp = mp # match played
        self.shots = shots # total shots
        self.shotsc = shotsc # total shots conceded
        self.tgc = tgc # total goals conceded
        self.r = [0,0,0] # WTL
        self.corners = corners

rspd = defaultdict(team)
for r in rsd:
    n,game_id,HomeTeam,AwayTeam,HomeScore,AwayScore,Home_xG,Away_xG,Home_shots,Away_shots,Home_corner,Away_corner,Home_PK_Goal,Away_PK_Goal,Home_PK_shots,Away_PK_shots,Home_ToP = r[:-4]
    homeWin = 3
    if (AwayScore > HomeScore): homeWin = 0
    elif (HomeScore > AwayScore): homeWin = 1
    elif (AwayScore == HomeScore): homewin = 2
    if (homeWin == 1):
        rspd[HomeTeam].score += 3
        rspd[HomeTeam].r[0] += 1
        rspd[AwayTeam].r[2] += 1
    elif (homeWin == 0):
        rspd[AwayTeam].score += 3
        rspd[HomeTeam].r[2] += 1
        rspd[AwayTeam].r[0] += 1
    else:
        rspd[HomeTeam].score += 1
        rspd[AwayTeam].score += 1
        rspd[HomeTeam].r[1] += 1
        rspd[AwayTeam].r[1] += 1
    rspd[HomeTeam].mph += 1
    rspd[HomeTeam].corners += int(Home_corner)
    rspd[AwayTeam].corners += int(Away_corner)
    rspd[AwayTeam].mpa += 1
    rspd[HomeTeam].tg += int(HomeScore)
    rspd[AwayTeam].tg += int(AwayScore)
    rspd[HomeTeam].tgc += int(AwayScore)
    rspd[AwayTeam].tgc += int(HomeScore)
    rspd[HomeTeam].tgah += int(AwayScore)
    rspd[AwayTeam].tgaa += int(HomeScore)
    rspd[HomeTeam].tp += float(Home_ToP)
    rspd[AwayTeam].tp += 1-float(Home_ToP)
    rspd[HomeTeam].txg += float(Home_xG)
    rspd[AwayTeam].txg += float(Away_xG)
    rspd[HomeTeam].shots += float(Home_shots)
    rspd[AwayTeam].shots += float(Away_shots)
    rspd[HomeTeam].shotsc += float(Away_shots)
    rspd[AwayTeam].shotsc += float(Home_shots)
    rspd[HomeTeam].mp += 1
    rspd[AwayTeam].mp += 1

rsppd = sorted(rspd, key=lambda x: rspd[x].score, reverse=True)
totalGoals = [rspd[i].tg for i in rsppd]
totalGoalsAgainst = [(rspd[i].tgaa+rspd[i].tgah) for i in rsppd]
avgPosession = [rspd[i].tp/rspd[i].mp for i in rsppd]
avgxG = [rspd[i].txg/rspd[i].mp for i in rsppd]
STGconversion = [rspd[i].tg/rspd[i].shots for i in rsppd]
shotQuality = [rspd[i].txg/rspd[i].shots for i in rsppd]
efficiency = [rspd[i].txg/rspd[i].tg for i in rsppd]
qualityP = [(rspd[i].corners+rspd[i].shots)/rspd[i].tp for i in rsppd]
defQuality = [rspd[i].tgc/rspd[i].shotsc for i in rsppd]

# All of the graphs are ranked by score.

#----Standings----

"1. Total Score (3 * Wins + Ties)"

# plt.bar(rsppd, score, label="Score")

"2. Team WTL"

# barWidth = 0.2
# br1 = np.arange(len(rsppd)) 
# br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 
# br4 = [x + barWidth for x in br3]
# score = [rspd[i].score for i in rsppd] 
# W = [rspd[i].r[0] for i in rsppd]
# T = [rspd[i].r[1] for i in rsppd]
# L = [rspd[i].r[2] for i in rsppd]
# plt.plot(br1, score, color='purple', marker='o', linestyle='-', linewidth=2, markersize=8, label='Score')
# plt.bar(br2, W, color ='b', width = barWidth, edgecolor ='grey', label ='W') 
# plt.bar(br3, T, color ='g', width = barWidth, edgecolor ='grey', label ='T') 
# plt.bar(br4, L, color ='r', width = barWidth, edgecolor ='grey', label ='L') 
# plt.xticks([r+barWidth for r in range(len(rsppd))], rsppd)

#----Offense----

"3. Shot Quality"

# plt.bar(rsppd, shotQuality, label='Shot Quality')
 
"4. Efficiency"

# plt.bar(rsppd, efficiency, label='Efficiency')

"5. Shots to Goals conversion"

# plt.bar(rsppd, STGconversion, label='Shot to goals conversion')

"6. Quality of Possession"

# plt.bar(rsppd, qualityP, label='Quality of Possession')

"7. Total Goals For"

# plt.bar(rsppd, totalGoals, label='Total Goals')

"8. Average Time of Possession"

# plt.bar(rsppd, avgPosession, label='Average Time of Possession')

"-. Average xG"

# plt.plot(avgxG, label='Average xG')

#----Defense----

"9. Defense Efficiency"

# plt.bar(rsppd, defQuality, label='Defensive Quality')

"10. Total Goals Against"

plt.bar(rsppd, totalGoalsAgainst, label='Total Goals Against')

# ----Rankings----

"-. Rating System (not finished)"

# elo = [(rspd[i].tg-rspd[i].tga+rspd[i].txg)/rspd[i].mp for i in rsppd]
# plt.plot(score, label='score')
# plt.plot(elo, label='elo')

10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010
# Labels

plt.xlabel('Rank')  
plt.ylabel('Values')
plt.legend()
plt.show()
