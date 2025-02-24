import csv


games = []
with open("../../outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

teams = []
with open("../../inputs/VBelo - teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = int(teams[i]['elo'])


def naia(year):
    matches = 0
    wins = 0

    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            t1_c = ''
            t2_c = ''
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    t1_c = teams[x]['conference']
                if games[i]['t2'] == teams[x]['short_name']:
                    t2_c = teams[x]['conference']
            if t1_c == 'NAIA' and games[i]['r_t1'] == '1':
                matches += 1
                wins += 1
            elif t2_c == 'NAIA' and games[i]['r_t2'] == '1':
                matches += 1
                wins += 1
            elif t1_c == 'NAIA' and games[i]['r_t1'] == '0':
                matches += 1
            elif t2_c == 'NAIA' and games[i]['r_t2'] == '0':
                matches += 1
    print(matches)
    print(wins)
    print(wins/matches)


naia('2024')
