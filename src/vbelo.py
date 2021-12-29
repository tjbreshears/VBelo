import csv
import math
import pandas as pd
import geopy.distance as gp

teams = []
with open("inputs/teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = int(teams[i]['elo'])

games = []
with open("inputs/games.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

# Resets static elo for D-III and NAIA teams
def static_elo ():
    for i in range(len(teams)):
        if teams[i]['division'] == 'D-III':
            teams[i]['elo'] = 1419
        elif teams[i]['division'] == 'NAIA':
            teams[i]['elo'] = 1373
        elif teams[i]['division'] == 'NCCAA':
            teams[i]['elo'] = 1373

# Function to calculate the Probability of winning/losing
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

# Function for calculating elo for a single game
def eloRating(game,K,t,current_season):

# Reverts elo to mean by 1/3 for new season
    if game['season'] != current_season:
        current_season = game['season']
        for i in range(len(teams)):
            teams[i]['elo'] = int(teams[i]['elo'])-((int(teams[i]['elo'])-1500)/3)

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

# Travel adjustment
# Minus t elo for every 500 miles traveled, limit of -25 eloRating
    global loc_home, loc_1, loc_2
    for i in range(len(teams)):
        if game['home'] == teams[i]['short_name']:
            loc_home = teams[i]['location']
        if game['team1'] == teams[i]['short_name']:
            loc_1 = teams[i]['location']
        if game['team2'] == teams[i]['short_name']:
            loc_2 = teams[i]['location']
    dist_1 = gp.distance(loc_home,loc_1).miles
    dist_2 = gp.distance(loc_home,loc_2).miles
    score1 = math.floor(dist_1/250) * t
    score2 = math.floor(dist_2/250) * t
    if score1 < -25:
        score1 = -25
    if score2 < -25:
        score2 = -25
    r1_adjust = r1_adjust + score1
    r2_adjust = r2_adjust + score2
    game['elo_adjusted_team1'] = r1_adjust
    game['elo_adjusted_team2'] = r2_adjust

# Calculate probabilities
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

#K value, Travel multiplier, first year in data
def season (K,t,season1):
    current_season = season1
    for i in range(len(games)):
        eloRating(games[i],K,t,current_season)
        current_season = games[i]['season']
    export_games (games)

def export_games (games):
    field_names = ['date','season','home','neutral','playoff','team1','team2','result_team1','result_team2','sets_team1','sets_team2','points_team1','points_team2','elo_start_team1','elo_start_team2','elo_adjusted_team1','elo_adjusted_team2','probability_team1','probability_team2','elo_end_team1','elo_end_team2']
    with open('outputs/games_output.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(games)

def top25 (teams):
    df = pd.DataFrame.from_dict(teams)
    df = df.sort_values(['elo'], ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df['elo'] = df['elo'].round(decimals = 0).astype(int)
    df.rename(columns = {'short_name':'School', 'elo':'Elo Rating'}, inplace = True)
    print(df[['School','Elo Rating']].head(25))

season(24,-1,'2021')
top25(teams)
