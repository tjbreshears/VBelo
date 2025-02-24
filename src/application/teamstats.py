import csv
import pandas as pd
import matplotlib.pyplot as plt
import json

# 'conf_wins','conf_losses','conf_pct'


def season_stats(year):
    teams = []
    with open(f"../../inputs/static/VBelo - teamstats_{year}.csv", 'r') as data:
        for line in csv.DictReader(data):
            teams.append(line)
        for i in range(len(teams)):
            teams[i]['elo'] = int(teams[i]['elo'])
            teams[i]['games'] = int(teams[i]['games'])
            teams[i]['wins'] = int(teams[i]['wins'])
            teams[i]['losses'] = int(teams[i]['losses'])
            teams[i]['win_pct'] = int(teams[i]['win_pct'])
            teams[i]['conf_wins'] = int(teams[i]['conf_wins'])
            teams[i]['conf_losses'] = int(teams[i]['conf_losses'])
            teams[i]['conf_pct'] = int(teams[i]['conf_pct'])
            teams[i]['home_wins'] = int(teams[i]['home_wins'])
            teams[i]['home_losses'] = int(teams[i]['home_losses'])
            teams[i]['home_pct'] = int(teams[i]['home_pct'])
            teams[i]['away_wins'] = int(teams[i]['away_wins'])
            teams[i]['away_losses'] = int(teams[i]['away_losses'])
            teams[i]['away_pct'] = int(teams[i]['away_pct'])
            teams[i]['sets_won'] = int(teams[i]['sets_won'])
            teams[i]['sets_lost'] = int(teams[i]['sets_lost'])
            teams[i]['set_diff'] = int(teams[i]['set_diff'])
            teams[i]['points_won'] = int(teams[i]['points_won'])
            teams[i]['points_lost'] = int(teams[i]['points_lost'])
            teams[i]['point_diff'] = int(teams[i]['point_diff'])
            teams[i]['soo'] = int(teams[i]['soo'])
            teams[i]['sos'] = int(teams[i]['sos'])
            teams[i]['cinco_wins'] = int(teams[i]['cinco_wins'])
            teams[i]['cinco_losses'] = int(teams[i]['cinco_losses'])
            teams[i]['cinco_pct'] = int(teams[i]['cinco_pct'])
            teams[i]['points_game'] = int(teams[i]['points_game'])
            teams[i]['points_set'] = int(teams[i]['points_set'])

    # points_game	points_set

    games = []
    with open("../../outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    for i in range(len(games)):
        print(i)
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    teams[x]['elo'] = round(float(games[i]['elo_end_team1']), 2)
                    teams[x]['games'] = int(teams[x]['games']) + 1
                    if games[i]['r_t1'] == '1':
                        teams[x]['wins'] = int(teams[x]['wins']) + 1
                    else:
                        teams[x]['losses'] = int(teams[x]['losses']) + 1
                    teams[x]['win_pct'] = '{0:.3f}'.format(int(teams[x]['wins'])/int(teams[x]['games']))
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t1'] == '1':
                        teams[x]['away_wins'] = int(teams[x]['away_wins']) + 1
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t1'] == '0':
                        teams[x]['away_losses'] = int(teams[x]['away_losses']) + 1
                    if int(teams[x]['away_wins'])+int(teams[x]['away_losses']) != 0:
                        teams[x]['away_pct'] = '{0:.3f}'.format(int(teams[x]['away_wins'])/(int(teams[x]['away_wins'])+int(teams[x]['away_losses'])))

                    teams[x]['sets_won'] = int(teams[x]['sets_won']) + int(games[i]['s_t1'])
                    teams[x]['sets_lost'] = int(teams[x]['sets_lost']) + int(games[i]['s_t2'])
                    teams[x]['set_diff'] = teams[x]['sets_won'] - teams[x]['sets_lost']
                    teams[x]['points_won'] = int(teams[x]['points_won']) + int(games[i]['p_t1'])
                    teams[x]['points_lost'] = int(teams[x]['points_lost']) + int(games[i]['p_t2'])
                    teams[x]['point_diff'] = teams[x]['points_won'] - teams[x]['points_lost']
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team2'])
                    teams[x]['sos'] = round(teams[x]['soo']/teams[x]['games'],2)
                    if (int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5) and games[i]['r_t1'] == '1':
                        teams[x]['cinco_wins'] = int(teams[x]['cinco_wins']) + 1
                    if (int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5) and games[i]['r_t1'] == '0':
                        teams[x]['cinco_losses'] = int(teams[x]['cinco_losses']) + 1
                    if int(teams[x]['cinco_wins'])+int(teams[x]['cinco_losses']) != 0:
                        teams[x]['cinco_pct'] = '{0:.3f}'.format(int(teams[x]['cinco_wins'])/(int(teams[x]['cinco_wins'])+int(teams[x]['cinco_losses'])))
                    teams[x]['points_game'] = round(teams[x]['point_diff']/teams[x]['games'], 2)
                    teams[x]['points_set'] = round(teams[x]['point_diff']/(teams[x]['sets_won']+teams[x]['sets_lost']), 2)

                if games[i]['t2'] == teams[x]['short_name']:
                    teams[x]['elo'] = round(float(games[i]['elo_end_team2']), 2)
                    teams[x]['games'] = int(teams[x]['games']) + 1
                    if games[i]['r_t2'] == '1':
                        teams[x]['wins'] = int(teams[x]['wins']) + 1
                    else:
                        teams[x]['losses'] = int(teams[x]['losses']) + 1
                    teams[x]['win_pct'] = '{0:.3f}'.format(int(teams[x]['wins'])/int(teams[x]['games']))
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t2'] == '1':
                        teams[x]['home_wins'] = int(teams[x]['home_wins']) + 1
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t2'] == '0':
                        teams[x]['home_losses'] = int(teams[x]['home_losses']) + 1
                    if int(teams[x]['home_losses'])+int(teams[x]['home_wins']) != 0:
                        teams[x]['home_pct'] = '{0:.3f}'.format(int(teams[x]['home_wins'])/(int(teams[x]['home_losses'])+int(teams[x]['home_wins'])))

                    teams[x]['sets_won'] = int(teams[x]['sets_won']) + int(games[i]['s_t2'])
                    teams[x]['sets_lost'] = int(teams[x]['sets_lost']) + int(games[i]['s_t1'])
                    teams[x]['set_diff'] = teams[x]['sets_won'] - teams[x]['sets_lost']
                    teams[x]['points_won'] = int(teams[x]['points_won']) + int(games[i]['p_t2'])
                    teams[x]['points_lost'] = int(teams[x]['points_lost']) + int(games[i]['p_t1'])
                    teams[x]['point_diff'] = int(teams[x]['points_won']) - int(teams[x]['points_lost'])
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team1'])
                    teams[x]['sos'] = round(teams[x]['soo']/teams[x]['games'],2)
                    if (int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5) and games[i]['r_t2'] == '1':
                        teams[x]['cinco_wins'] = int(teams[x]['cinco_wins']) + 1
                    if (int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5) and games[i]['r_t2'] == '0':
                        teams[x]['cinco_losses'] = int(teams[x]['cinco_losses']) + 1
                    if int(teams[x]['cinco_wins'])+int(teams[x]['cinco_losses']) != 0:
                        teams[x]['cinco_pct'] = '{0:.3f}'.format(int(teams[x]['cinco_wins'])/(int(teams[x]['cinco_wins'])+int(teams[x]['cinco_losses'])))
                    teams[x]['points_game'] = round(teams[x]['point_diff']/teams[x]['games'],2)
                    teams[x]['points_set'] = round(teams[x]['point_diff']/(teams[x]['sets_won']+teams[x]['sets_lost']), 2)

        field_names = ['short_name', 'full_name', 'division', 'conference', 'elo', 'games', 'wins', 'losses', 'win_pct',
                       'conf_wins', 'conf_losses', 'conf_pct', 'home_wins', 'home_losses', 'home_pct', 'away_wins',
                       'away_losses', 'away_pct', 'sets_won', 'sets_lost', 'set_diff', 'points_won', 'points_lost',
                       'point_diff', 'soo', 'sos', 'cinco_wins', 'cinco_losses', 'cinco_pct', 'points_game',
                       'points_set']
        with open(f'../../outputs/teamstats_output_{year}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(teams)
    #    json_object_teams = json.dumps(teams, indent = 4)
    #    with open("outputs/teams_2023.json", "w") as outfile:
    #        outfile.write(json_object_teams)


season_stats('2023')
