#Mean Square Error for elo model

import csv
import numpy as np
import vbelo

# MSE for K values
def mse_k ():
    best = [1,1]
    for K in range (0,50):
        vbelo.season (K,-10,'2021')
        games = []
        with open("outputs/games_output.csv", 'r') as data:
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
        vbelo.season (24,t,'2021')
        games = []
        with open("outputs/games_output.csv", 'r') as data:
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
            vbelo.season (K,t,'2021')
            games = []
            with open("outputs/games_output.csv", 'r') as data:
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
def mse_current ():
    vbelo.season (30,-1,'2020')
    games = []
    with open("outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    expected = []
    actual = []

    for i in range(len(games)):
        if games[i]['season'] == '2022' and games[i]['r_t1'] != '':
            expected.append(float(games[i]['probability_team1']))
            expected.append(float(games[i]['probability_team2']))
            actual.append(float(games[i]['r_t1']))
            actual.append(float(games[i]['r_t2']))

    mse = np.square(np.subtract(expected,actual)).mean()
    print(f'Current RSE: {mse}')

#mse_k()
#mse_t()
#mse_kt()
mse_current()
