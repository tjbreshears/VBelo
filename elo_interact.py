""" TODO
[if team not tracked, elo reverts to start]

Write to games to CSV
Write tracked teams to CSV
"""

import csv
import math

teams = []
with open("inputs/teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)

games = []
with open("inputs/games_2021.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

#set initial elo for every team based on divison/conference
for i in range(len(teams)):
    teams[i]['elo'] = 1350
    if teams[i]['division'] == 'NAIA':
        teams[i]['elo'] = 1000
    elif teams[i]['division'] == 'D-III':
        teams[i]['elo'] = 1100
    elif teams[i]['conference'] == 'Carolinas' or\
     teams[i]['conference'] =='SIAC' or\
     teams[i]['conference'] =='Independent':
        teams[i]['elo'] = 1200

# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

#function for calculating elo
def eloRating(game):    #was t1,t2,d
    K = 30 #still working to find an ideal K

    for i in range(len(teams)):
        if game['team1'] == teams[i]['short_name']:
            r1 = teams[i]['elo']
            game['elo_start_team1'] = r1
    for i in range(len(teams)):
        if game['team2'] == teams[i]['short_name']:
            r2 = teams[i]['elo']
            game['elo_start_team2'] = r2

    p1 = probability(r2, r1)
    game['probability_team1'] = p1
    p2 = probability(r1, r2)
    game['probability_team2'] = p2

    if game['result_team1'] == '1':
        r1 = r1 + K * (1 - p1)
        r2 = r2 + K * (0 - p2)
    elif game['result_team2'] == '1':
        r1 = r1 + K * (0 - p1)
        r2 = r2 + K * (1 - p2)
    else:
        pass

    game['elo_end_team1'] = r1
    game['elo_end_team2'] = r2

#updates elo on teams list
    for i in range(len(teams)):
        if game['team1'] == teams[i]['short_name']:
            teams[i]['elo'] = r1
    for i in range(len(teams)):
        if game['team2'] == teams[i]['short_name']:
            teams[i]['elo'] = r2

def season ():
    for i in range(len(games)):
        eloRating(games[i])

season()
print(games)
