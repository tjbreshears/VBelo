import csv
import random
import math
import geopy.distance as gp

teams = []
with open("outputs/teams_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = float(teams[i]['elo'])

games = []
with open("inputs/VBelo - NC_MC.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

Hawaii,Greenville,Ball,USC,Penn,UCLA,LBSU = 0,0,0,0,0,0,0

def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def eloRating(game,K,t):
    global Hawaii,Greenville,Ball,USC,Penn,UCLA,LBSU
    global r1_start,r2_start,r1_adjust,r2_adjust,r1_end,r2_end
    for i in range(len(teams)):
        if game['t1'] == teams[i]['short_name']:
            r1_start = teams[i]['elo']
            game['elo_start_team1'] = r1_start
    for i in range(len(teams)):
        if game['t2'] == teams[i]['short_name']:
            r2_start = teams[i]['elo']
            game['elo_start_team2'] = r2_start

#sets adjusted elo in case there is no adjusted needed
#will probably be removed when travel is added
    game['elo_adjusted_team1'] = r1_start
    game['elo_adjusted_team2'] = r2_start
    r1_adjust = r1_start
    r2_adjust = r2_start

#home court advantage
    if game['home'] == game['t2']:
        r2_adjust = r2_start + 50
        game['elo_adjusted_team2'] = r2_adjust
    elif game['home'] == game['t1']:
        r1_adjust = r1_start + 50
        game['elo_adjusted_team1'] = r2_adjust

# Travel adjustment
# Minus t elo for every 500 miles traveled, limit of -25 eloRating
    global loc_home, loc_1, loc_2
    for i in range(len(teams)):
        if game['home'] == teams[i]['short_name']:
            loc_home = teams[i]['location']
        if game['t1'] == teams[i]['short_name']:
            loc_1 = teams[i]['location']
        if game['t2'] == teams[i]['short_name']:
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

# Monte Carlo part
    random_outcome = random.random()

    if game['date'] == '1' and p1 > 0.5 and random_outcome < p1:
        games[2]['t2'] = game['t1']
    elif game['date'] == '1' and p1 > 0.5 and random_outcome > p1:
        games[2]['t2'] = game['t2']
    elif game['date'] == '1' and p1 < 0.5 and random_outcome > p2:
        games[2]['t2'] = game['t1']
    elif game['date'] == '1' and p1 < 0.5 and random_outcome < p2:
        games[2]['t2'] = game['t2']


    if game['date'] == '2' and p1 > 0.5 and random_outcome < p1:
        games[4]['t2'] = game['t1']
    elif game['date'] == '2' and p1 > 0.5 and random_outcome > p1:
        games[4]['t2'] = game['t2']
    elif game['date'] == '2' and p1 < 0.5 and random_outcome > p2:
        games[4]['t2'] = game['t1']
    elif game['date'] == '2' and p1 < 0.5 and random_outcome < p2:
        games[4]['t2'] = game['t2']

    if game['date'] == '3' and p1 > 0.5 and random_outcome < p1:
        games[3]['t2'] = game['t1']
    elif game['date'] == '3' and p1 > 0.5 and random_outcome > p1:
        games[3]['t2'] = game['t2']
    elif game['date'] == '3' and p1 < 0.5 and random_outcome > p2:
        games[3]['t2'] = game['t1']
    elif game['date'] == '3' and p1 < 0.5 and random_outcome < p2:
        games[3]['t2'] = game['t2']

    if game['date'] == '4' and p1 > 0.5 and random_outcome < p1:
        games[5]['t1'] = game['t1']
    elif game['date'] == '4' and p1 > 0.5 and random_outcome > p1:
        games[5]['t1'] = game['t2']
    elif game['date'] == '4' and p1 < 0.5 and random_outcome > p2:
        games[5]['t1'] = game['t1']
    elif game['date'] == '4' and p1 < 0.5 and random_outcome < p2:
        games[5]['t1'] = game['t2']

    if game['date'] == '5' and p1 > 0.5 and random_outcome < p1:
        games[5]['t2'] = game['t1']
    elif game['date'] == '5' and p1 > 0.5 and random_outcome > p1:
        games[5]['t2'] = game['t2']
    elif game['date'] == '5' and p1 < 0.5 and random_outcome > p2:
        games[5]['t2'] = game['t1']
    elif game['date'] == '5' and p1 < 0.5 and random_outcome < p2:
        games[5]['t2'] = game['t2']

    if game['date'] == '6' and p1 > 0.5 and random_outcome < p1:
        if game['t1'] == 'Hawaii':
            Hawaii += 1
        elif game['t1'] == 'Greenville':
            Greenville += 1
        elif game['t1'] == 'Ball':
            Ball += 1
        elif game['t1'] == 'USC':
            USC += 1
        elif game['t1'] == 'Penn':
            Penn += 1
        elif game['t1'] == 'UCLA':
            UCLA += 1
        elif game['t1'] == 'LBSU':
            LBSU += 1
    elif game['date'] == '6' and p1 > 0.5 and random_outcome > p1:
        if game['t2'] == 'Hawaii':
            Hawaii += 1
        elif game['t2'] == 'Greenville':
            Greenville += 1
        elif game['t2'] == 'Ball':
            Ball += 1
        elif game['t2'] == 'USC':
            USC += 1
        elif game['t2'] == 'Penn':
            Penn += 1
        elif game['t2'] == 'UCLA':
            UCLA += 1
        elif game['t2'] == 'LBSU':
            LBSU += 1
    elif game['date'] == '6' and p1 < 0.5 and random_outcome > p2:
        if game['t1'] == 'Hawaii':
            Hawaii += 1
        elif game['t1'] == 'Greenville':
            Greenville += 1
        elif game['t1'] == 'Ball':
            Ball += 1
        elif game['t1'] == 'USC':
            USC += 1
        elif game['t1'] == 'Penn':
            Penn += 1
        elif game['t1'] == 'UCLA':
            UCLA += 1
        elif game['t1'] == 'LBSU':
            LBSU += 1
    elif game['date'] == '6' and p1 < 0.5 and random_outcome < p2:
        if game['t2'] == 'Hawaii':
            Hawaii += 1
        elif game['t2'] == 'Greenville':
            Greenville += 1
        elif game['t2'] == 'Ball':
            Ball += 1
        elif game['t2'] == 'USC':
            USC += 1
        elif game['t2'] == 'Penn':
            Penn += 1
        elif game['t2'] == 'UCLA':
            UCLA += 1
        elif game['t2'] == 'LBSU':
            LBSU += 1

def post_season (K,t):
    for i in range(len(games)):
        eloRating(games[i],K,t)


def monte_carlo (sims):
    for i in range(sims):
        post_season(30,-1)
    HawaiiP = "{:.2%}".format(Hawaii/sims)
    GreenvilleP = "{:.2%}".format(Greenville/sims)
    BallP = "{:.2%}".format(Ball/sims)
    USCP = "{:.2%}".format(USC/sims)
    PennP = "{:.2%}".format(Penn/sims)
    UCLAP = "{:.2%}".format(UCLA/sims)
    LBSUP = "{:.2%}".format(LBSU/sims)
    print(f"Hawai'i: {HawaiiP}")
    print(f"NGU: {GreenvilleP}")
    print(f"Ball State: {BallP}")
    print(f"USC: {USCP}")
    print(f"Penn State: {PennP}")
    print(f"UCLA: {UCLAP}")
    print(f"Long Beach: {LBSUP}")

monte_carlo(10000)
