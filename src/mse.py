#Mean Square Error for elo model

import csv
import numpy as np

def mse ():
    games = []
    with open("outputs/games_2021_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    expected = []
    actual = []

    for i in range(len(games)):
        if games[i]['result_team1'] != '':
            expected.append(float(games[i]['probability_team1']))
            expected.append(float(games[i]['probability_team2']))
            actual.append(float(games[i]['result_team1']))
            actual.append(float(games[i]['result_team2']))

    mse = np.square(np.subtract(expected,actual)).mean()
    print(f'Mean Square Error: {mse}')

mse ()
