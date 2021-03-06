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

nt_wins = 0
nt_games = 0

def finder ():
    global nt_wins,nt_games
    for x in range(len(games)):
        team1 = games[x]['team1']
        team2 = games[x]['team2']
        for one in range(len(teams)):
            for two in range(len(teams)):
                if (team1 == teams[one]['short_name'] and teams[one]['tracking'] == '0') and (team2 == teams[two]['short_name'] and teams[two]['tracking'] != '0') and (games[x]['result_team1'] != ''):
                    nt_games += 1
                    nt_wins += int(games[x]['result_team1'])
                elif (team1 == teams[one]['short_name'] and teams[one]['tracking'] != '0') and (team2 == teams[two]['short_name'] and teams[two]['tracking'] == '0') and (games[x]['result_team1'] != ''):
                    nt_games += 1
                    nt_wins += int(games[x]['result_team2'])

    print(f"Non-Tracked Win Percentage: {nt_wins/nt_games}")

#function solving for rating 2, instead of Probability
#calibrates elo rating equal to historical winning percentage of non-tracked teams.
def prob(avg, p):
    print(f"Non-tracked base elo: {((400.0 * (math.log10((1/p)-1)))-avg) * -1}" )

finder()
prob(1500,nt_wins/nt_games)
