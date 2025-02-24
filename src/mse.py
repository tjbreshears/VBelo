#Mean Square Error for elo model

import csv
import numpy as np
# import vbelo

# MSE for K values
def mse_k ():
    best = [1,1]
    for K in range (0,100):
        vbelo.season (K, -10, '2021')
        games = []
        with open("../outputs/games_output.csv", 'r') as data:
            for line in csv.DictReader(data):
                games.append(line)

        expected = []
        actual = []

        for i in range(len(games)):
            if games[i]['r_t1'] != '':
                expected.append(float(games[i]['probability_team1']))
                expected.append(float(games[i]['probability_team2']))
                actual.append(float(games[i]['r_t1']))
                actual.append(float(games[i]['r_t2']))

        mse = np.square(np.subtract(expected,actual)).mean()
        if mse < best[1]:
            best[0] = K
            best[1] = mse
    print(f'Best K: {best[0]}')
    print(f'Best RSE: {best[1]}')

# MSE for travel variable values
def mse_t ():
    best = [1,1]
    for t in range (-20,0):
        vbelo.season (24, t, '2021')
        games = []
        with open("../outputs/games_output.csv", 'r') as data:
            for line in csv.DictReader(data):
                games.append(line)

        expected = []
        actual = []

        for i in range(len(games)):
            if games[i]['r_t1'] != '':
                expected.append(float(games[i]['probability_team1']))
                expected.append(float(games[i]['probability_team2']))
                actual.append(float(games[i]['r_t1']))
                actual.append(float(games[i]['r_t2']))

        mse = np.square(np.subtract(expected,actual)).mean()
        if mse < best[1]:
            best[0] = t
            best[1] = mse
    print(f'Best t: {best[0]}')
    print(f'Best RSE: {best[1]}')

# MSE for K and travel variable values
def mse_kt ():
    best = [1,1,1]
    for K in range (16,36):
        for t in range (-20,0):
            vbelo.season (K, t, '2021')
            games = []
            with open("../outputs/games_output.csv", 'r') as data:
                for line in csv.DictReader(data):
                    games.append(line)

            expected = []
            actual = []

            for i in range(len(games)):
                if games[i]['r_t1'] != '':
                    expected.append(float(games[i]['probability_team1']))
                    expected.append(float(games[i]['probability_team2']))
                    actual.append(float(games[i]['r_t1']))
                    actual.append(float(games[i]['r_t2']))

            mse = np.square(np.subtract(expected,actual)).mean()
            if mse < best[2]:
                best[0] = K
                best[1] = t
                best[2] = mse
    print(f'Best K: {best[0]}')
    print(f'Best t: {best[1]}')
    print(f'Best RSE: {best[2]}')


# MSE for one set of input variables
def mse_current(year):

    games = []
    with open("../outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    expected = []
    actual = []

    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            expected.append(float(games[i]['probability_team1']))
            expected.append(float(games[i]['probability_team2']))
            actual.append(float(games[i]['r_t1']))
            actual.append(float(games[i]['r_t2']))

    mse = np.square(np.subtract(expected,actual)).mean()
    print(f'Current MSE: {mse}')


def mse_current_di(year):
    teams = []
    with open("../inputs/VBelo - teams.csv", 'r') as data:
        for line in csv.DictReader(data):
            teams.append(line)

    games = []
    with open("../outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    matches = []
    for game in games:
        if game['season'] == year and game['r_t1'] != '':
            t1 = game['t1']
            t2 = game['t2']
            t1e = ''
            t2e = ''

            for team in teams:
                if team['short_name'] == t1:
                    t1e = team['eligible']
            for team in teams:
                if team['short_name'] == t2:
                    t2e = team['eligible']
            if t1e == '1' and t2e == '1':
                matches.append(game)

    expected = []
    actual = []

    for i in range(len(matches)):
        if matches[i]['season'] == year and matches[i]['r_t1'] != '':
            expected.append(float(matches[i]['probability_team1']))
            expected.append(float(matches[i]['probability_team2']))
            actual.append(float(matches[i]['r_t1']))
            actual.append(float(matches[i]['r_t2']))

    mse = np.square(np.subtract(expected,actual)).mean()
    print(f'Current MSE-DI: {mse}')


# mse_k()
# mse_t()
# mse_kt()
mse_current('2024')
mse_current_di('2024')
