import csv
import config


def conference(year):
    teams = []
    with open("inputs/VBelo - teams.csv", 'r') as data:
        for line in csv.DictReader(data):
            teams.append(line)

    games = []
    with open("outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    stats = []
    with open(f"outputs/teamstats_output_{year}.csv", 'r') as data:
        for line in csv.DictReader(data):
            stats.append(line)
        for i in range(len(stats)):
            stats[i]['conf_wins'] = int(stats[i]['conf_wins'])
            stats[i]['conf_losses'] = int(stats[i]['conf_losses'])
            stats[i]['conf_pct'] = float(stats[i]['conf_pct'])

    matches = []
    for game in games:
        if game['season'] == year and game['r_t1'] != '':
            t1 = game['t1']
            t2 = game['t2']
            t1c = ''
            t2c = ''

            for team in teams:
                if team['short_name'] == t1:
                    t1c = team['conference']
            for team in teams:
                if team['short_name'] == t2:
                    t2c = team['conference']
            if t1c == t2c:
                matches.append(game)

    for match in matches:
        t1 = match['t1']
        t2 = match['t2']

        for stat in stats:
            if stat['short_name'] == t1 and match['r_t1'] == '1':
                stat['conf_wins'] += 1
            if stat['short_name'] == t2 and match['r_t1'] == '1':
                stat['conf_losses'] += 1
            if stat['short_name'] == t1 and match['r_t2'] == '1':
                stat['conf_losses'] += 1
            if stat['short_name'] == t2 and match['r_t2'] == '1':
                stat['conf_wins'] += 1

    for item in stats:
        if item['conf_wins'] + item['conf_losses'] != 0:
            item['conf_pct'] = '{0:.3f}'.format(item['conf_wins'] / (item['conf_wins'] + item['conf_losses']))
        else:
            item['conf_pct'] = '{0:.3f}'.format(0)

    # save to csv
    field_names = ['short_name', 'full_name', 'division', 'conference', 'elo', 'games', 'wins', 'losses', 'win_pct',
                   'conf_wins', 'conf_losses', 'conf_pct', 'home_wins', 'home_losses', 'home_pct', 'away_wins',
                   'away_losses', 'away_pct', 'sets_won', 'sets_lost', 'set_diff', 'points_won', 'points_lost',
                   'point_diff', 'soo', 'sos', 'cinco_wins', 'cinco_losses', 'cinco_pct', 'points_game',
                   'points_set']
    with open(f'outputs/teamstats_output_{year}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(stats)


conference(config.current_year)
