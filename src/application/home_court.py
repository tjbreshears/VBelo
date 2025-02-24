import csv
import config

games = []
with open("../../outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

def home_wins (year):
    wins = 0
    losses = 0
    home_favored = 0
    away_favored = 0
    home_favored_wins = 0
    home_favored_losses = 0
    away_favored_wins = 0
    away_favored_losses = 0
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '1':
            wins += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '0':
            losses += 1
        if games[i]['season'] == year and games[i]['n'] == '0' and games[i]['probability_team2'] > games[i]['probability_team1']:
            home_favored += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['probability_team2'] < games[i]['probability_team1']:
            away_favored += 1
        if games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '1' and games[i]['probability_team2'] > games[i]['probability_team1']:
            home_favored_wins += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '0' and games[i]['probability_team2'] > games[i]['probability_team1']:
            home_favored_losses += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '1' and games[i]['probability_team2'] < games[i]['probability_team1']:
            away_favored_losses += 1
        elif games[i]['season'] == year and games[i]['n'] == '0' and games[i]['r_t2'] == '0' and games[i]['probability_team2'] < games[i]['probability_team1']:
            away_favored_wins += 1
    print(wins/(wins+losses))
    print(wins+losses)
    print(wins)
    print(f'Home Favored: {home_favored}')
    print(f'Away Favored: {away_favored}')
    print(f'Home Favored Wins: {home_favored_wins}')
    print(f'Home Favored Losses: {home_favored_losses}')
    print(f'Away Favored Wins: {away_favored_wins}')
    print(f'Away Favored Losses: {away_favored_losses}')

home_wins(config.current_year)
