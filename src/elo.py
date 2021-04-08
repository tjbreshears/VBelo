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
def eloRating(game,K):    #was t1,t2,d

    static_elo ()
    global r1_start,r2_start,r1_adjust,r2_adjust,r1_end,r2_end
    for i in range(len(teams)):
        if game['team1'] == teams[i]['short_name']:
            r1_start = teams[i]['elo']
            game['elo_start_team1'] = r1_start
    for i in range(len(teams)):
        if game['team2'] == teams[i]['short_name']:
            r2_start = teams[i]['elo']
            game['elo_start_team2'] = r2_start

#sets adjusted elo in case there is no adjusted needed
#will probably be removed when travel is added
    game['elo_adjusted_team1'] = r1_start
    game['elo_adjusted_team2'] = r2_start
    r1_adjust = r1_start
    r2_adjust = r2_start

#home court advantage
#home teams are always listed as team2 in input
    if game['home'] == game['team2']:
        r2_adjust = r2_start + 70
        game['elo_adjusted_team2'] = r2_adjust

    p1 = probability(r2_adjust, r1_adjust)
    game['probability_team1'] = p1
    p2 = probability(r1_adjust, r2_adjust)
    game['probability_team2'] = p2

    if game['result_team1'] == '1':
        d1 = int(game['sets_team1'])-int(game['sets_team2'])
        d2 = int(game['sets_team2'])
        r1_end = r1_start + K * (1 - p1) + (K/6 * (d1/3))
        r2_end = r2_start + K * (0 - p2) + (K/6 * (d2/3))
    elif game['result_team2'] == '1':
        d1 = int(game['sets_team2'])-int(game['sets_team1'])
        d2 = int(game['sets_team1'])
        r1_end = r1_start + K * (0 - p1) + (K/6 * (d1/3))
        r2_end = r2_start + K * (1 - p2) + (K/6 * (d2/3))
    else:
        r1_end = r1_start
        r2_end = r2_start

    game['elo_end_team1'] = r1_end
    game['elo_end_team2'] = r2_end

#updates elo on teams list
    for i in range(len(teams)):
        if game['team1'] == teams[i]['short_name']:
            teams[i]['elo'] = r1_end
    for i in range(len(teams)):
        if game['team2'] == teams[i]['short_name']:
            teams[i]['elo'] = r2_end

def season (K):
    for i in range(len(games)):
        eloRating(games[i],K)
    export_teams (teams)
    export_games (games)

season(24)
