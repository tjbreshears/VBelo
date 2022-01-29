import csv
import pandas as pd
import matplotlib.pyplot as plt

teams = []
with open("inputs/VBelo - teams - 2022.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
    for i in range(len(teams)):
        teams[i]['pd'] = int(teams[i]['pd'])

games = []
with open("outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

def season_stats (year):
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    if games[i]['r_t1'] == '1':
                        teams[x]['w'] = int(teams[x]['w']) + 1
                    else:
                        teams[x]['l'] = int(teams[x]['l']) + 1
                    teams[x]['sf'] = int(teams[x]['sf']) + int(games[i]['s_t1'])
                    teams[x]['sa'] = int(teams[x]['sa']) + int(games[i]['s_t2'])
                    teams[x]['sd'] = teams[x]['sf'] - teams[x]['sa']
                    teams[x]['pf'] = int(teams[x]['pf']) + int(games[i]['p_t1'])
                    teams[x]['pa'] = int(teams[x]['pa']) + int(games[i]['p_t2'])
                    teams[x]['pd'] = teams[x]['pf'] - teams[x]['pa']
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team2'])
                if games[i]['t2'] == teams[x]['short_name']:
                    if games[i]['r_t2'] == '1':
                        teams[x]['w'] = int(teams[x]['w']) + 1
                    else:
                        teams[x]['l'] = int(teams[x]['l']) + 1
                    teams[x]['sf'] = int(teams[x]['sf']) + int(games[i]['s_t2'])
                    teams[x]['sa'] = int(teams[x]['sa']) + int(games[i]['s_t1'])
                    teams[x]['sd'] = teams[x]['sf'] - teams[x]['sa']
                    teams[x]['pf'] = int(teams[x]['pf']) + int(games[i]['p_t2'])
                    teams[x]['pa'] = int(teams[x]['pa']) + int(games[i]['p_t1'])
                    teams[x]['pd'] = int(teams[x]['pf']) - int(teams[x]['pa'])
                    teams[x]['soo'] = float(teams[x]['soo']) + float(games[i]['elo_start_team1'])
        export_teams_season(teams)

def export_teams_season (teams):
    field_names = ['short_name','full_name','division','conference','w','l','sf','sa','sd','pf','pa','pd','soo']
    with open('outputs/teams_output_2022.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(teams)

season_stats('2022')
