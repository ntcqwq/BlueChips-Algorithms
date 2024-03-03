import csv, itertools, numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

file_path = "/Users/nchen26/kitchen/BlueChips-Algorithms/NSL_Regular_Season_Data.csv"

with open(file_path, newline='') as rsrd:
    reader = csv.reader(rsrd)
    rsd = list(reader)


def normalize(arr):
    def n(x, l) -> float:
        return (l[x]-min(l))/(max(l)-min(l))
    ans = []
    for i in range(len(arr)):
        ans.append(n(i, arr)*20)
    return ans


# OOP
names = rsd.pop(0)
class team:
    def __init__(self, score=0, scorea=0, scoreh=0, mpa=0, mph=0, tg=0, tga=0, tgh=0, tgc=0, tgca=0, tgch=0, tp=0, tpa=0, tph=0, txg=0, txga=0, txgh=0, mp=0, shots=0, shotsa=0, shotsh=0, shotsca=0, shotsc=0, corners=0, pens=0, shotsch=0, txgca=0, txgc=0, txgch=0, cornersh=0, cornersa=0, pensa=0, pensh=0):
        self.score = score 
        self.scorea = scorea
        self.scoreh = scoreh
        self.mp = mp # match played
        self.mpa = mpa # match played away
        self.mph = mph # match played home
        self.tg = tg # total goals
        self.tga = tga # total goals away
        self.tgh = tgh # total goals home
        self.tgc = tgc # total goals conceded
        self.tgca = tgca # total goals conceded away
        self.tgch = tgch # total goals conceded home
        self.tp = tp # total possession
        self.tpa = tpa # total possession away
        self.tph = tph # total possession home
        self.txg = txg # total xG
        self.txga = txga # total xG away
        self.txgh = txgh # total xG home
        self.txgc = txgc # total c.xG
        self.txgca = txgca # total c. xG away
        self.txgch = txgch # total c. xG home
        self.shots = shots # total shots
        self.shotsa = shotsa # total shots away
        self.shotsh = shotsh # total shots home
        self.shotsc = shotsc # total shots conceded
        self.shotsca = shotsca # total shots conceded away
        self.shotsch = shotsch # total shots conceded home
        self.r = [0,0,0] # WTL
        self.ra = [0,0,0] # WTL away
        self.rh = [0,0,0] # WTL home
        self.corners = corners
        self.cornersa = cornersa
        self.cornersh = cornersh
        self.pens = pens
        self.pensa = pensa
        self.pensh = pensh

rspd = defaultdict(team)
for r in rsd:
    n,game_id,HomeTeam,AwayTeam,HomeScore,AwayScore,Home_xG,Away_xG,Home_shots,Away_shots,Home_corner,Away_corner,Home_PK_Goal,Away_PK_Goal,Home_PK_shots,Away_PK_shots,Home_ToP = r[:-4]
    homeWin = 3
    if (AwayScore > HomeScore): homeWin = 0
    elif (HomeScore > AwayScore): homeWin = 1
    elif (AwayScore == HomeScore): homewin = 2
    if (homeWin == 1):
        rspd[HomeTeam].score += 3
        rspd[HomeTeam].scoreh += 3
        rspd[HomeTeam].r[0] += 1
        rspd[AwayTeam].r[2] += 1
        rspd[HomeTeam].rh[0] += 1
        rspd[AwayTeam].ra[2] += 1
    elif (homeWin == 0):
        rspd[AwayTeam].scorea += 3
        rspd[AwayTeam].score += 3
        rspd[HomeTeam].r[2] += 1
        rspd[AwayTeam].r[0] += 1
        rspd[HomeTeam].rh[2] += 1
        rspd[AwayTeam].ra[0] += 1
    else:
        rspd[HomeTeam].score += 1
        rspd[HomeTeam].scoreh += 1
        rspd[AwayTeam].score += 1
        rspd[AwayTeam].scorea += 1
        rspd[HomeTeam].r[1] += 1
        rspd[AwayTeam].r[1] += 1
        rspd[HomeTeam].rh[1] += 1
        rspd[AwayTeam].ra[1] += 1
    rspd[HomeTeam].mp += 1
    rspd[AwayTeam].mp += 1
    rspd[HomeTeam].mph += 1
    rspd[AwayTeam].mpa += 1

    rspd[HomeTeam].tg += int(HomeScore)
    rspd[AwayTeam].tg += int(AwayScore)
    rspd[HomeTeam].tgh += int(HomeScore)
    rspd[AwayTeam].tga += int(AwayScore)

    rspd[HomeTeam].tgc += int(AwayScore)
    rspd[AwayTeam].tgc += int(HomeScore)
    rspd[HomeTeam].tgch += int(AwayScore)
    rspd[AwayTeam].tgca += int(HomeScore)

    rspd[HomeTeam].tp += float(Home_ToP)
    rspd[AwayTeam].tp += 1-float(Home_ToP)
    rspd[HomeTeam].tph += float(Home_ToP)
    rspd[AwayTeam].tpa += 1-float(Home_ToP)

    rspd[HomeTeam].txg += float(Home_xG)
    rspd[AwayTeam].txg += float(Away_xG)
    rspd[HomeTeam].txgh += float(Home_xG)
    rspd[AwayTeam].txga += float(Away_xG)

    rspd[HomeTeam].txgc += float(Away_xG)
    rspd[AwayTeam].txgc += float(Home_xG)
    rspd[HomeTeam].txgch += float(Away_xG)
    rspd[AwayTeam].txgca += float(Home_xG)

    rspd[HomeTeam].shots += float(Home_shots)
    rspd[AwayTeam].shots += float(Away_shots)
    rspd[HomeTeam].shotsh += float(Home_shots)
    rspd[AwayTeam].shotsa += float(Away_shots)

    rspd[HomeTeam].shotsc += float(Away_shots)
    rspd[AwayTeam].shotsc += float(Home_shots)
    rspd[HomeTeam].shotsch += float(Away_shots)
    rspd[AwayTeam].shotsca += float(Home_shots)

    rspd[HomeTeam].corners += int(Home_corner)
    rspd[AwayTeam].corners += int(Away_corner)
    rspd[HomeTeam].cornersh += int(Home_corner)
    rspd[AwayTeam].cornersa += int(Away_corner)

    rspd[HomeTeam].pens += float(Home_PK_shots)
    rspd[AwayTeam].pens += float(Away_PK_shots)
    rspd[HomeTeam].pensh += float(Home_PK_shots)
    rspd[AwayTeam].pensa += float(Away_PK_shots)

rsppd = sorted(rspd, key=lambda x: rspd[x].score, reverse=True)

totalGoals = [rspd[i].tg for i in rsppd]
totalGoalsH = [rspd[i].tgh for i in rsppd]
totalGoalsA = [rspd[i].tga for i in rsppd]
totalGoalsC = [rspd[i].tgc for i in rsppd]
totalGoalsCH = [rspd[i].tgch for i in rsppd]
totalGoalsCA = [rspd[i].tgca for i in rsppd]
totalPossession = [rspd[i].tp for i in rsppd]
totalPossessionH = [rspd[i].tph for i in rsppd]
totalPossessionA = [rspd[i].tpa for i in rsppd]
totalxG = [rspd[i].txg for i in rsppd]
totalxGH = [rspd[i].txgh for i in rsppd]
totalxGA = [rspd[i].txga for i in rsppd]
totalxGC = [rspd[i].txgc for i in rsppd]
totalxGCH = [rspd[i].txgch for i in rsppd]
totalxGCA = [rspd[i].txgca for i in rsppd]
StGConversion = [rspd[i].tg/rspd[i].shots for i in rsppd]
StGConversionH = [rspd[i].tgh/rspd[i].shotsh for i in rsppd]
StGConversionA = [rspd[i].tga/rspd[i].shotsa for i in rsppd]
shotQuality = [(rspd[i].txg-rspd[i].pens*0.78)/rspd[i].shots for i in rsppd]
shotQualityH = [(rspd[i].txgh-rspd[i].pensh*0.78)/rspd[i].shotsh for i in rsppd]
shotQualityA = [(rspd[i].txga-rspd[i].pensa*0.78)/rspd[i].shotsa for i in rsppd]
efficiency = [(rspd[i].txg-rspd[i].pens*0.78)/rspd[i].tg for i in rsppd]
efficiencyH = [(rspd[i].txgh-rspd[i].pensh*0.78)/rspd[i].tgh for i in rsppd]
efficiencyA = [(rspd[i].txga-rspd[i].pensa*0.78)/rspd[i].tga for i in rsppd]
qualityP = [(rspd[i].corners+rspd[i].shots)/rspd[i].tp for i in rsppd]
qualityPH = [(rspd[i].cornersh+rspd[i].shotsh)/rspd[i].tph for i in rsppd]
qualityPA = [(rspd[i].cornersa+rspd[i].shotsa)/rspd[i].tpa for i in rsppd]
defQuality = [rspd[i].tgc/rspd[i].shotsc for i in rsppd]
defQualityH = [rspd[i].tgch/rspd[i].shotsch for i in rsppd]
defQualityA = [rspd[i].tgca/rspd[i].shotsca for i in rsppd]
score = [rspd[i].score for i in rsppd]
scoreH = [rspd[i].scoreh for i in rsppd]
scoreA = [rspd[i].scorea for i in rsppd] 
shotsConceded = [rspd[i].shotsc for i in rsppd]
shotsConcededH = [rspd[i].shotsch for i in rsppd]
shotsConcededA = [rspd[i].shotsca for i in rsppd]
W = [rspd[i].r[0] for i in rsppd]
T = [rspd[i].r[1] for i in rsppd]
L = [rspd[i].r[2] for i in rsppd]
W_h = [rspd[i].rh[0] for i in rsppd]
T_h = [rspd[i].rh[1] for i in rsppd]
L_h = [rspd[i].rh[2] for i in rsppd]
W_a = [rspd[i].ra[0] for i in rsppd]
T_a = [rspd[i].ra[1] for i in rsppd]
L_a = [rspd[i].ra[2] for i in rsppd]
goalDifferential = [(rspd[i].tg-rspd[i].tgc) for i in rsppd]
goalDifferentialH = [(rspd[i].tgh-rspd[i].tgch) for i in rsppd]
goalDifferentialA = [(rspd[i].tga-rspd[i].tgca) for i in rsppd]

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

# plt.bar(rsppd, avgxG, label='Average xG')

"-. Average xG against"

# plt.bar(rsppd, avgxGa, label='Average xG against')

#----Defense----

"9. Defense Efficiency"

# plt.bar(rsppd, defQuality, label='Defensive Quality')

"10. Total Goals Against"

# plt.bar(rsppd, totalGoalsAgainst, label='Total Goals Against')


"-. Total Shots Conceded"

# plt.bar(rsppd, shotsconceded, label='Shots Conceded')


# ----Rankings----

"-. Rating System (not finished)"

# print(normalize(defQuality))
# elo = [(rspd[rsppd[i]].tg-rspd[rsppd[i]].tgc)+(normalize(defQuality)[i]) for i in range(len(rsppd))]
# score2 = [rspd[i].r[0]-rspd[i].r[2] for i in rsppd]
# plt.bar(rsppd, elo, label='elo')
# plt.plot(score2, label='score')

10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010
# Labels

# plt.xlabel('Rank')  
# plt.ylabel('Values')
# plt.legend()
# plt.show()


def writeResults():
    def n(x, l) -> float:
        return (l[x]-min(l))/(max(l)-min(l))
    with open('/Users/nchen26/kitchen/BlueChips-Algorithms/results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        f_names = ['totalGoals', 'totalGoalsH', 'totalGoalsA', 'totalGoalsC', 'totalGoalsCH','totalGoalsCA', 'totalPossession', 'totalPossessionH', 'totalPossessionA', 'totalxG', 'totalxGH', 'totalxGA', 'totalxGC', 'totalxGCH', 'totalxGCA', 'StGConversion', 'StGConversionH', 'StGConversionA', 'shotQuality', 'shotQualityH', 'shotQualityA', 'efficiency', 'efficiencyH', 'efficiencyA', 'qualityP', 'qualityPH', 'qualityPA', 'defQuality', 'defQualityH', 'defQualityA', 'score', 'scoreH', 'scoreA', 'shotsConceded', 'shotsConcededH', 'shotsConcededA', 'W', 'T', 'L', 'W_h', 'T_h', 'L_h', 'W_a', 'T_a', 'L_a', 'goalDifferential', 'goalDifferentialH', 'goalDifferentialA']
        spamwriter.writerow(f_names)
        for i in enumerate(rsppd):
            j = i[0]
            ans = [i[1]]
            for name in [totalGoals, totalGoalsH, totalGoalsA, totalGoalsC, totalGoalsCH, totalGoalsCA, totalPossession, totalPossessionH, totalPossessionA, totalxG, totalxGH, totalxGA, totalxGC, totalxGCH, totalxGCA, StGConversion, StGConversionH, StGConversionA, shotQuality, shotQualityH, shotQualityA, efficiency, efficiencyH, efficiencyA, qualityP, qualityPH, qualityPA, defQuality, defQualityH, defQualityA, score, scoreH, scoreA, shotsConceded, shotsConcededH, shotsConcededA, W, T, L, W_h, T_h, L_h, W_a, T_a, L_a, goalDifferential, goalDifferentialH, goalDifferentialA]:
                ans.append(n(j, name))
            spamwriter.writerow(ans)

writeResults()

