import csv

import elo
import mse

teams = []
with open("inputs/teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)

games = []
with open("inputs/games_2021.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

#set initial elo for every team 1500 - the hopeful average
for i in range(len(teams)):
    teams[i]['elo'] = 1500

for i in range (1,51):
    print(f'K = {i}')
    elo.season (i)
    mse.mse()
