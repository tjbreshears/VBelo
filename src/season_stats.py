import csv
import pandas as pd
import matplotlib.pyplot as plt
import json

teams = []
with open("inputs/VBelo - teams - 2022.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
    for i in range(len(teams)):
        teams[i]['point_diff'] = int(teams[i]['point_diff'])

games = []
with open("outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

# 'conf_wins','conf_losses','conf_pct'

def season_stats (year):
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    teams[x]['elo'] = round(float(games[i]['elo_end_team1']),2)
                    teams[x]['games'] = int(teams[x]['games']) + 1
                    if games[i]['r_t1'] == '1':
                        teams[x]['wins'] = int(teams[x]['wins']) + 1
                    else:
                        teams[x]['losses'] = int(teams[x]['losses']) + 1
                    teams[x]['win_pct'] = round(int(teams[x]['wins'])/int(teams[x]['games']),3)
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t1'] == '1':
                        teams[x]['away_wins'] = int(teams[x]['away_wins']) + 1
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t1'] == '0':
                        teams[x]['away_losses'] = int(teams[x]['away_losses']) + 1
                    if int(teams[x]['away_wins'])+int(teams[x]['away_losses']) != 0:
                        teams[x]['away_pct'] = round(int(teams[x]['away_wins'])/(int(teams[x]['away_wins'])+int(teams[x]['away_losses'])),3)

                    teams[x]['sets_won'] = int(teams[x]['sets_won']) + int(games[i]['s_t1'])
                    teams[x]['sets_lost'] = int(teams[x]['sets_lost']) + int(games[i]['s_t2'])
                    teams[x]['set_diff'] = teams[x]['sets_won'] - teams[x]['sets_lost']
                    teams[x]['points_won'] = int(teams[x]['points_won']) + int(games[i]['p_t1'])
                    teams[x]['points_lost'] = int(teams[x]['points_lost']) + int(games[i]['p_t2'])
                    teams[x]['point_diff'] = teams[x]['points_won'] - teams[x]['points_lost']
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team2'])
                    teams[x]['sos'] = round(teams[x]['soo']/teams[x]['games'],2)
                if games[i]['t2'] == teams[x]['short_name']:
                    teams[x]['elo'] = round(float(games[i]['elo_end_team2']),2)
                    teams[x]['games'] = int(teams[x]['games']) + 1
                    if games[i]['r_t2'] == '1':
                        teams[x]['wins'] = int(teams[x]['wins']) + 1
                    else:
                        teams[x]['losses'] = int(teams[x]['losses']) + 1
                    teams[x]['win_pct'] = round(int(teams[x]['wins'])/int(teams[x]['games']),3)
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t2'] == '1':
                        teams[x]['home_wins'] = int(teams[x]['home_wins']) + 1
                    if games[i]['home'] == games[i]['t2'] and games[i]['r_t2'] == '0':
                        teams[x]['home_losses'] = int(teams[x]['home_losses']) + 1
                    if int(teams[x]['home_losses'])+int(teams[x]['home_wins']) != 0:
                        teams[x]['home_pct'] = round(int(teams[x]['home_wins'])/(int(teams[x]['home_losses'])+int(teams[x]['home_wins'])),3)

                    teams[x]['sets_won'] = int(teams[x]['sets_won']) + int(games[i]['s_t2'])
                    teams[x]['sets_lost'] = int(teams[x]['sets_lost']) + int(games[i]['s_t1'])
                    teams[x]['set_diff'] = teams[x]['sets_won'] - teams[x]['sets_lost']
                    teams[x]['points_won'] = int(teams[x]['points_won']) + int(games[i]['p_t2'])
                    teams[x]['points_lost'] = int(teams[x]['points_lost']) + int(games[i]['p_t1'])
                    teams[x]['point_diff'] = int(teams[x]['points_won']) - int(teams[x]['points_lost'])
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team1'])
                    teams[x]['sos'] = teams[x]['soo']/teams[x]['games']
        export_teams_season(teams)

def export_teams_season (teams):
    field_names = ['short_name','full_name','division','conference','elo','games','wins','losses','win_pct','conf_wins','conf_losses','conf_pct','home_wins','home_losses','home_pct','away_wins','away_losses','away_pct','sets_won','sets_lost','set_diff','points_won','points_lost','point_diff','soo','sos']
    with open('outputs/teams_output_2022.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(teams)
    json_object_teams = json.dumps(teams, indent = 4)
    with open("outputs/teams_2022.json", "w") as outfile:
        outfile.write(json_object_teams)

season_stats('2022')
