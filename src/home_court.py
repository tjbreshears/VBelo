import csv

games = []
with open("outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

def home_wins (year):
    wins = 0
    losses = 0
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '1':
            wins += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '0':
            losses += 1
    print(wins/(wins+losses))
    print(wins+losses)

home_wins('2022')
