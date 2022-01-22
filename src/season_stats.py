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
        if games[i]['season'] == year and games[i]['result_team1'] != '':
            for x in range(len(teams)):
                if games[i]['team1'] == teams[x]['short_name']:
                    if games[i]['result_team1'] == '1':
                        teams[x]['w'] = int(teams[x]['w']) + 1
                    else:
                        teams[x]['l'] = int(teams[x]['l']) + 1
                    teams[x]['sf'] = int(teams[x]['sf']) + int(games[i]['sets_team1'])
                    teams[x]['sa'] = int(teams[x]['sa']) + int(games[i]['sets_team2'])
                    teams[x]['sd'] = teams[x]['sf'] - teams[x]['sa']
                    teams[x]['pf'] = int(teams[x]['pf']) + int(games[i]['points_team1'])
                    teams[x]['pa'] = int(teams[x]['pa']) + int(games[i]['points_team2'])
                    teams[x]['pd'] = teams[x]['pf'] - teams[x]['pa']
                if games[i]['team2'] == teams[x]['short_name']:
                    if games[i]['result_team2'] == '1':
                        teams[x]['w'] = int(teams[x]['w']) + 1
                    else:
                        teams[x]['l'] = int(teams[x]['l']) + 1
                    teams[x]['sf'] = int(teams[x]['sf']) + int(games[i]['sets_team2'])
                    teams[x]['sa'] = int(teams[x]['sa']) + int(games[i]['sets_team1'])
                    teams[x]['sd'] = teams[x]['sf'] - teams[x]['sa']
                    teams[x]['pf'] = int(teams[x]['pf']) + int(games[i]['points_team2'])
                    teams[x]['pa'] = int(teams[x]['pa']) + int(games[i]['points_team1'])
                    teams[x]['pd'] = int(teams[x]['pf']) - int(teams[x]['pa'])
        export_teams_season(teams)

def export_teams_season (teams):
    field_names = ['short_name','full_name','division','conference','w','l','sf','sa','sd','pf','pa','pd']
    with open('outputs/teams_output_2022.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(teams)

def top_stats (teams):
    df = pd.DataFrame.from_dict(teams)
    df = df.sort_values(['pd'], ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df.rename(columns = {'full_name':'School', 'pd':'Point Differential'}, inplace = True)
    df.index.name = "Rank"
    rank = df[['School','Point Differential']].head(19)

    # Table
    fig, ax = plt.subplots(dpi=200)
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
#    plt.title('Point Differential - 2022', loc='center',pad='40',size='x-large',family='Cambria',weight='bold')
    table = ax.table(cellText=rank.values, colLabels=rank.columns, loc='center',rowLabels=rank.index)
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(rank.columns))))
    cells = table.properties()["celld"]
    for i in range(0, 20):
        cells[i, 1].set_text_props(ha="center")

    #display table
    fig.tight_layout()
    plt.show()

season_stats('2022')
