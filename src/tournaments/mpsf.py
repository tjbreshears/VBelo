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
with open("inputs/Tournaments - MPSF.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

#8 team modified playoff bracket
#teams by seeds
seed1 = 'UCLA'
seed2 = 'x'
seed3 = 'x'
seed4 = 'x'
seed5 = 'x'
seed6 = 'x'

#winning
seed1_win, seed2_win, seed3_win, seed4_win, seed5_win, seed6_win, seed7_win = 0,0,0,0,0,0,0

#making finals
seed1_finals, seed2_finals, seed3_finals, seed4_finals, seed5_finals, seed6_finals, seed7_finals = 0,0,0,0,0,0,0

#making the semis
seed2_semis, seed3_semis, seed4_semis, seed5_semis, seed6_semis, seed7_semis = 0,0,0,0,0,0


def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def eloRating(game,K,t):
    global seed1_win, seed2_win, seed3_win, seed4_win, seed5_win, seed6_win
    global seed1_finals, seed2_finals, seed3_finals, seed4_finals, seed5_finals, seed6_finals
    global seed3_semis, seed4_semis, seed5_semis, seed6_semis

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

#game 1: 2 vs 7 (quarterfinals)
    if game['date'] == '1' and p1 > 0.5 and random_outcome < p1:
        games[4]['t1'] = game['t1']
        seed2_semis += 1
    elif game['date'] == '1' and p1 > 0.5 and random_outcome > p1:
        games[3]['t2'] = game['t2']
        seed7_semis += 1
    elif game['date'] == '1' and p1 < 0.5 and random_outcome > p2:
        games[4]['t1'] = game['t1']
        seed2_semis += 1
    elif game['date'] == '1' and p1 < 0.5 and random_outcome < p2:
        games[3]['t2'] = game['t2']
        seed7_semis += 1

#game 2: 3 vs 6 (quarterfinals)
    if game['date'] == '2' and p1 > 0.5 and random_outcome < p1:
        if games[4]['t1'] == seed2:
            games[4]['t2'] = game['t1']
        elif:
            games[4]['t1'] = game['t1']
        seed3_semis += 1
    elif game['date'] == '2' and p1 > 0.5 and random_outcome > p1:
        if games[3]['t2'] == seed7:
            games[4]['t2'] = game['t2']
        elif:
            games[3]['t2'] = game['t2']
        seed6_semis += 1
    elif game['date'] == '2' and p1 < 0.5 and random_outcome > p2:
        if games[4]['t1'] == seed2:
            games[4]['t2'] = game['t1']
        elif:
            games[4]['t1'] = game['t1']
        seed3_semis += 1
    elif game['date'] == '2' and p1 < 0.5 and random_outcome < p2:
        if games[3]['t2'] == seed7:
            games[4]['t2'] = game['t2']
        elif:
            games[3]['t2'] = game['t2']
        seed6_semis += 1

#game 3: 4 vs 5 (quarterfinals)
    if game['date'] == '3' and p1 > 0.5 and random_outcome < p1:
        if games[3]['t2'] == '':
            games[3]['t2'] = game['t1']
        elif games[4]['t1'] == '':
            games[4]['t1'] = game['t1']
        elif games[4]['t2'] == '':
            games[4]['t2'] = game['t1']
        seed4_semis += 1
    elif game['date'] == '3' and p1 > 0.5 and random_outcome > p1:
        if games[3]['t2'] == '':
            games[3]['t2'] = game['t2']
        elif games[4]['t1'] == '':
            games[4]['t1'] = game['t2']
        elif games[4]['t2'] == '':
            games[4]['t2'] = game['t2']
        seed5_semis += 1
    elif game['date'] == '3' and p1 < 0.5 and random_outcome > p2:
        if games[3]['t2'] == '':
            games[3]['t2'] = game['t1']
        elif games[4]['t1'] == '':
            games[4]['t1'] = game['t1']
        elif games[4]['t2'] == '':
            games[4]['t2'] = game['t1']
        seed4_semis += 1
    elif game['date'] == '3' and p1 < 0.5 and random_outcome < p2:
        if games[3]['t2'] == '':
            games[3]['t2'] = game['t2']
        elif games[4]['t1'] == '':
            games[4]['t1'] = game['t2']
        elif games[4]['t2'] == '':
            games[4]['t2'] = game['t2']
        seed5_semis += 1

#game 4: 1 vs 4/5/6/7 (semifinals)
    if game['date'] == '4' and p1 > 0.5 and random_outcome < p1:
        games[5]['t1'] = game['t1']
        seed1_finals += 1
    elif game['date'] == '4' and p1 > 0.5 and random_outcome > p1:
        games[5]['t1'] = game['t2']
        if game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
        elif game['t2'] == seed6:
            seed6_finals += 1
        elif game['t2'] == seed7:
            seed7_finals += 1
    elif game['date'] == '4' and p1 < 0.5 and random_outcome > p2:
        games[5]['t1'] = game['t2']
        if game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
        elif game['t2'] == seed6:
            seed6_finals += 1
        elif game['t2'] == seed7:
            seed7_finals += 1
    elif game['date'] == '4' and p1 < 0.5 and random_outcome < p2:
        games[5]['t1'] = game['t2']
        if game['t2'] == seed3:
            seed3_finals += 1
        elif game['t2'] == seed6:
            seed6_finals += 1

#game 5: 2/3/4/5 vs 3/4/5/6 (semifinals)
    if game['date'] == '5' and p1 > 0.5 and random_outcome < p1:
        games[5]['t2'] = game['t1']
        if game['t2'] == seed2:
            seed2_finals += 1
        elif game['t2'] == seed3:
            seed3_finals += 1
        elif game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
    elif game['date'] == '5' and p1 > 0.5 and random_outcome > p1:
        games[5]['t2'] = game['t2']
        if game['t2'] == seed3:
            seed3_finals += 1
        elif game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
        elif game['t2'] == seed6:
            seed6_finals += 1
    elif game['date'] == '5' and p1 < 0.5 and random_outcome > p2:
        games[5]['t2'] = game['t1']
        if game['t2'] == seed2:
            seed2_finals += 1
        elif game['t2'] == seed3:
            seed3_finals += 1
        elif game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
    elif game['date'] == '5' and p1 < 0.5 and random_outcome < p2:
        games[5]['t2'] = game['t2']
        if game['t2'] == seed3:
            seed3_finals += 1
        elif game['t2'] == seed4:
            seed4_finals += 1
        elif game['t2'] == seed5:
            seed5_finals += 1
        elif game['t2'] == seed6:
            seed6_finals += 1

#game 6: 1/4/5/6/7 vs 2/3/4/5/6 (finals)
    if game['date'] == '6' and p1 > 0.5 and random_outcome < p1:
        if game['t1'] == seed1:
            seed1_win += 1
        elif game['t1'] == seed4:
            seed4_win += 1
        elif game['t1'] == seed5:
            seed5_win += 1
        elif game['t1'] == seed6:
            seed6_win += 1
        elif game['t1'] == seed7:
            seed7_win += 1
    elif game['date'] == '6' and p1 > 0.5 and random_outcome > p1:
        if game['t2'] == seed2:
            seed2_win += 1
        elif game['t2'] == seed3:
            seed3_win += 1
        elif game['t2'] == seed4:
            seed4_win += 1
        elif game['t2'] == seed5:
            seed5_win += 1
        elif game['t2'] == seed6:
            seed6_win += 1
    elif game['date'] == '6' and p1 < 0.5 and random_outcome > p2:
        if game['t1'] == seed1:
            seed1_win += 1
        elif game['t1'] == seed4:
            seed4_win += 1
        elif game['t1'] == seed5:
            seed5_win += 1
        elif game['t1'] == seed6:
            seed6_win += 1
        elif game['t1'] == seed7:
            seed7_win += 1
    elif game['date'] == '6' and p1 < 0.5 and random_outcome < p2:
        if game['t2'] == seed2:
            seed2_win += 1
        elif game['t2'] == seed3:
            seed3_win += 1
        elif game['t2'] == seed4:
            seed4_win += 1
        elif game['t2'] == seed5:
            seed5_win += 1
        elif game['t2'] == seed6:
            seed6_win += 1

def post_season (K,t):
    for i in range(len(games)):
        eloRating(games[i],K,t)


def monte_carlo (sims):
    for i in range(sims):
        semis_pool = []
        post_season(30,-1)

#formatting for printing (the hard way)
    seed1_win_p = "{:.2%}".format(seed1_win/sims)
    seed2_win_p = "{:.2%}".format(seed2_win/sims)
    seed3_win_p = "{:.2%}".format(seed3_win/sims)
    seed4_win_p = "{:.2%}".format(seed4_win/sims)
    seed5_win_p = "{:.2%}".format(seed5_win/sims)
    seed6_win_p = "{:.2%}".format(seed6_win/sims)
    seed7_win_p = "{:.2%}".format(seed7_win/sims)

    seed1_finals_p = "{:.2%}".format(seed1_finals/sims)
    seed2_finals_p = "{:.2%}".format(seed2_finals/sims)
    seed3_finals_p = "{:.2%}".format(seed3_finals/sims)
    seed4_finals_p = "{:.2%}".format(seed4_finals/sims)
    seed5_finals_p = "{:.2%}".format(seed5_finals/sims)
    seed6_finals_p = "{:.2%}".format(seed6_finals/sims)
    seed7_finals_p = "{:.2%}".format(seed7_finals/sims)

    seed2_semis_p = "{:.2%}".format(seed2_semis/sims)
    seed3_semis_p = "{:.2%}".format(seed3_semis/sims)
    seed4_semis_p = "{:.2%}".format(seed4_semis/sims)
    seed5_semis_p = "{:.2%}".format(seed5_semis/sims)
    seed6_semis_p = "{:.2%}".format(seed6_semis/sims)
    seed7_semis_p = "{:.2%}".format(seed7_semis/sims)


    print(f"{seed1} (1): 100%, {seed1_finals_p}, {seed1_win_p}")
    print(f"{seed2} (2): {seed2_semis_p}, {seed2_finals_p}, {seed2_win_p}")
    print(f"{seed3} (3): {seed3_semis_p}, {seed3_finals_p}, {seed3_win_p}")
    print(f"{seed4} (4): {seed4_semis_p}, {seed4_finals_p}, {seed4_win_p}")
    print(f"{seed5} (5): {seed5_semis_p}, {seed5_finals_p}, {seed5_win_p}")
    print(f"{seed6} (6): {seed6_semis_p}, {seed6_finals_p}, {seed6_win_p}")
    print(f"{seed7} (7): {seed7_semis_p}, {seed6_finals_p}, {seed6_win_p}")


monte_carlo(50000)
