import csv
import math
from export_data import export_teams
from export_data import export_games

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

def static_elo ():
    for i in range(len(teams)):
        if teams[i]['division'] == 'D-III':
            teams[i]['elo'] = 1419
        elif teams[i]['division'] == 'NAIA':
            teams[i]['elo'] = 1373

# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

#function for calculating elo
def eloRating(game):    #was t1,t2,d
    K = 32 #still working to find an ideal K

    static_elo ()

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
        d1 = int(game['sets_team1'])-int(game['sets_team2'])
        d2 = int(game['sets_team2'])
        r1 = r1 + K * (1 - p1) + (K/6 * (d1/3))
        r2 = r2 + K * (0 - p2) + (K/6 * (d2/3))
    elif game['result_team2'] == '1':
        d1 = int(game['sets_team2'])-int(game['sets_team1'])
        d2 = int(game['sets_team1'])
        r1 = r1 + K * (0 - p1) + (K/6 * (d1/3))
        r2 = r2 + K * (1 - p2) + (K/6 * (d2/3))
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
    export_teams (teams)
    export_games (games)

season()
