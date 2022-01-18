import csv

games = []
with open("outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

teams = []
with open("inputs/VBelo - teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = int(teams[i]['elo'])

def tweet(date):
    text = 'Daily #VBelo Predictions: ' + date + '\n'
    for i in range(len(games)):
        if date in games[i]['date']:
            team1 = games[i]['team1']
            team1p = round(float(games[i]['probability_team1'])*100)
            team2 = games[i]['team2']
            team2p = round(float(games[i]['probability_team2'])*100)
            for x in range(len(teams)):
                if games[i]['team1'] == teams[x]['short_name']:
                    team1 = teams[x]['twitter']
                if games[i]['team2'] == teams[x]['short_name']:
                    team2 = teams[x]['twitter']
            text += (f'{team1} ({team1p}%) vs {team2} ({team2p}%)\n')
    print(text)
tweet('1/18/2022')
