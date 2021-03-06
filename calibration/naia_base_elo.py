#Disclaimer: there is not enough historical data for NAIA to really work.
#This is more of a test to show how it will work with more data.

import math
import csv

teams = []
with open("inputs/teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)

games = []
with open("inputs/games_2021.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

#Since no NAIA teams won in dataset, I added 0.25 to the wins to avoid
#divide by zero error. Makes current win percentage 0.05
naia_wins = 0.25
naia_games = 0

def finder ():
    global naia_wins,naia_games
    for x in range(len(games)):
        team1 = games[x]['team1']
        team2 = games[x]['team2']
        for i in range(len(teams)):
            if teams[i]['short_name'] == team1 and teams[i]['conference'] == 'NAIA':
                naia_games += 1
                naia_wins += int(games[x]['result_team1'])
            elif teams[i]['short_name'] == team2 and teams[i]['conference'] == 'NAIA':
                naia_games += 1
                naia_wins += int(games[x]['result_team2'])
    print(f"NAIA Win Percentage: {naia_wins/naia_games}")

#function solving for rating 2, instead of Probability
#calibrates elo rating equal to historical winning percentage of NAIA teams
def prob(avg, p):
    print(f"NAIA base elo: {((400.0 * (math.log10((1/p)-1)))-avg) * -1}" )

finder()
prob(1500,naia_wins/naia_games)
