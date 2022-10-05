import csv
import pandas as pd
import matplotlib.pyplot as plt

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

not_tracked = ['D-III','NAIA','NCCAA','n/a']

start_data = {'Conference':['Big West','Carolinas','EIVA','Independent','MIVA','MPSF','NEC','SIAC'],
'Non-Conf Matches':[0,0,0,0,0,0,0,0],'Non-Conf Wins':[0,0,0,0,0,0,0,0],'Non-Conf Losses':[0,0,0,0,0,0,0,0],
'Non-Conf Home Matches':[0,0,0,0,0,0,0,0],'Non-Conf Home Wins':[0,0,0,0,0,0,0,0],'Non-Conf Home Losses':[0,0,0,0,0,0,0,0],
'Non-Conf Away Matches':[0,0,0,0,0,0,0,0],'Non-Conf Away Wins':[0,0,0,0,0,0,0,0],'Non-Conf Away Losses':[0,0,0,0,0,0,0,0],
'Non-Conf Neutral Matches':[0,0,0,0,0,0,0,0],'Non-Conf Neutral Wins':[0,0,0,0,0,0,0,0],'Non-Conf Neutral Losses':[0,0,0,0,0,0,0,0],
}

df = pd.DataFrame(start_data)
df=df.set_index('Conference')

def stats (year):
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            t1_c = ''
            t2_c = ''
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    t1_c = teams[x]['conference']
                if games[i]['t2'] == teams[x]['short_name']:
                    t2_c = teams[x]['conference']
            if t1_c != t2_c:
                if t1_c not in not_tracked:
                    df.loc[t1_c,'Non-Conf Matches'] += 1
                    df.loc[t1_c,'Non-Conf Wins'] += int(games[i]['r_t1'])
                    if games[i]['r_t1'] == '0':
                        df.loc[t1_c,'Non-Conf Losses'] += 1
                    if games[i]['n'] == '0':
                        df.loc[t1_c,'Non-Conf Away Matches'] += 1
                        df.loc[t1_c,'Non-Conf Away Wins'] += int(games[i]['r_t1'])
                        if games[i]['r_t1'] == '0':
                            df.loc[t1_c,'Non-Conf Away Losses'] += 1
                    if games[i]['n'] == '1':
                        df.loc[t1_c,'Non-Conf Neutral Matches'] += 1
                        df.loc[t1_c,'Non-Conf Neutral Wins'] += int(games[i]['r_t1'])
                        if games[i]['r_t1'] == '0':
                            df.loc[t1_c,'Non-Conf Neutral Losses'] += 1
                if t2_c not in not_tracked:
                    df.loc[t2_c,'Non-Conf Matches'] += 1
                    df.loc[t2_c,'Non-Conf Wins'] += int(games[i]['r_t2'])
                    if games[i]['r_t2'] == '0':
                        df.loc[t2_c,'Non-Conf Losses'] += 1
                    if games[i]['n'] == '0':
                        df.loc[t2_c,'Non-Conf Home Matches'] += 1
                        df.loc[t2_c,'Non-Conf Home Wins'] += int(games[i]['r_t2'])
                        if games[i]['r_t2'] == '0':
                            df.loc[t2_c,'Non-Conf Home Losses'] += 1
                    if games[i]['n'] == '1':
                        df.loc[t2_c,'Non-Conf Neutral Matches'] += 1
                        df.loc[t2_c,'Non-Conf Neutral Wins'] += int(games[i]['r_t2'])
                        if games[i]['r_t2'] == '0':
                            df.loc[t2_c,'Non-Conf Neutral Losses'] += 1

    pd.set_option('display.max_columns', None)
    df.to_csv('outputs/conference_stats_2022.csv')

stats('2022')
