import csv
import math
import pandas as pd
import geopy.distance as gp
import matplotlib.pyplot as plt
import json

teams = []
with open("inputs/VBelo - teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = int(teams[i]['elo'])

games = []
with open("inputs/VBelo - games.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

old_date = ''
tracking = []

# Resets static elo for D-III and NAIA teams
def static_elo ():
    for i in range(len(teams)):
        if teams[i]['division'] == 'D-III':
            teams[i]['elo'] = 1419
        elif teams[i]['division'] == 'NAIA':
            teams[i]['elo'] = 1373
        elif teams[i]['division'] == 'NCCAA':
            teams[i]['elo'] = 1373

# Function to calculate the Probability of winning/losing
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

# Function for calculating elo for a single game
def eloRating(game,K,t,current_season):
    global last_date
    global new_date
    global old_date
    global year_stats
    if game['r_t1'] == '':
        pass
    else:
        last_date = game['date'].split(' ',1)[0]

# Between season reversion
# First team's elo is reduced by a max of 15% by accounting for attrition
# Second all teams revert to the mean by 1/6
    if game['season'] != current_season:
        year_stats = game['season']
        current_season = game['season']
        ret_year = "ret_" + current_season
        for i in range(len(teams)):
            max_loss = float(teams[i]['elo']) * 0.05
            actual_loss = max_loss * (float(teams[i][ret_year]))
            teams[i]['elo'] = teams[i]['elo'] - actual_loss
            teams[i]['elo'] = int(teams[i]['elo'])-((int(teams[i]['elo'])-1500)/10)

# Sets elo for new teams for their first season
        if current_season == '2022':
            for i in range(len(teams)):
                if teams[i]['short_name'] == 'American' or \
                teams[i]['short_name'] == 'Benedict' or \
                teams[i]['short_name'] == 'Central' or \
                teams[i]['short_name'] == 'Edward' or \
                teams[i]['short_name'] == 'Fairleigh' or \
                teams[i]['short_name'] == 'Fort Valley' or \
                teams[i]['short_name'] == 'KSU' or \
                teams[i]['short_name'] == 'LIU' or \
                teams[i]['short_name'] == 'Maryville' or \
                teams[i]['short_name'] == 'Morehouse':
                    teams[i]['elo'] = 1419
        elif current_season == '2023':
            for i in range(len(teams)):
                if teams[i]['short_name'] == 'MST' or \
                teams[i]['short_name'] == 'Merrimack':
                    teams[i]['elo'] = 1419


#lifetime tracking of each team's elo
    new_date = game['date'].split(' ',1)[0]

    if old_date == new_date:
        pass
    elif old_date != new_date and game['r_t1'] != '':
        new_date_dict = {}
        for i in range(len(teams)):
            new_date_dict['date'] = new_date
            if teams[i]['eligible'] == '1':
                new_date_dict[teams[i]['short_name']] = teams[i]['elo']
        tracking.append(new_date_dict)
        old_date = new_date

    static_elo ()
    global r1_start,r2_start,r1_adjust,r2_adjust,r1_end,r2_end
    for i in range(len(teams)):
        if game['t1'] == teams[i]['short_name']:
            r1_start = teams[i]['elo']
            game['elo_start_team1'] = r1_start
    for i in range(len(teams)):
        if game['t2'] == teams[i]['short_name']:
            r2_start = teams[i]['elo']
            game['elo_start_team2'] = r2_start

#sets adjusted elo in case there is no adjusted needed
#will probably be removed when travel is added
    game['elo_adjusted_team1'] = r1_start
    game['elo_adjusted_team2'] = r2_start
    r1_adjust = r1_start
    r2_adjust = r2_start

#home court advantage
#home teams are always listed as team2 in input
    if game['home'] == game['t2']:
        r2_adjust = r2_start + 50
        game['elo_adjusted_team2'] = r2_adjust

# Travel adjustment
# Minus t elo for every 500 miles traveled, limit of -25 eloRating
    global loc_home, loc_1, loc_2
    for i in range(len(teams)):
        if game['home'] == teams[i]['short_name']:
            loc_home = teams[i]['location']
        if game['t1'] == teams[i]['short_name']:
            loc_1 = teams[i]['location']
        if game['t2'] == teams[i]['short_name']:
            loc_2 = teams[i]['location']
    dist_1 = gp.distance(loc_home,loc_1).miles
    dist_2 = gp.distance(loc_home,loc_2).miles
    score1 = math.floor(dist_1/250) * t
    score2 = math.floor(dist_2/250) * t
    if score1 < -25:
        score1 = -25
    if score2 < -25:
        score2 = -25
    r1_adjust = r1_adjust + score1
    r2_adjust = r2_adjust + score2
    game['elo_adjusted_team1'] = r1_adjust
    game['elo_adjusted_team2'] = r2_adjust

# Calculate probabilities
    p1 = probability(r2_adjust, r1_adjust)
    game['probability_team1'] = p1
    p2 = probability(r1_adjust, r2_adjust)
    game['probability_team2'] = p2

    if game['r_t1'] == '1':
        d1 = int(game['s_t1'])-int(game['s_t2'])
        d2 = int(game['s_t2'])
        r1_end = r1_start + K * (1 - p1) + (K/6 * (d1/3))
        r2_end = r2_start + K * (0 - p2) + (K/6 * (d2/3))
    elif game['r_t2'] == '1':
        d1 = int(game['s_t2'])-int(game['s_t1'])
        d2 = int(game['s_t1'])
        r1_end = r1_start + K * (0 - p1) + (K/6 * (d1/3))
        r2_end = r2_start + K * (1 - p2) + (K/6 * (d2/3))
    else:
        r1_end = r1_start
        r2_end = r2_start

    game['elo_end_team1'] = r1_end
    game['elo_end_team2'] = r2_end

#updates elo on teams list
    for i in range(len(teams)):
        if game['t1'] == teams[i]['short_name']:
            teams[i]['elo'] = r1_end
    for i in range(len(teams)):
        if game['t2'] == teams[i]['short_name']:
            teams[i]['elo'] = r2_end

#K value, Travel multiplier, first year in data
def season (K,t,season1):
    current_season = season1
    for i in range(len(games)):
        eloRating(games[i],K,t,current_season)
        current_season = games[i]['season']
    export_games (games)
    export_teams (teams)
    export_tracking (tracking)

def export_games (games):
    field_names = ['date','season','home','n','p','t1','t2','r_t1','r_t2','s_t1','s_t2','p_t1','p_t2','s1_t1','s1_t2','s2_t1','s2_t2','s3_t1','s3_t2','s4_t1','s4_t2','s5_t1','s5_t2','elo_start_team1','elo_start_team2','elo_adjusted_team1','elo_adjusted_team2','probability_team1','probability_team2','elo_end_team1','elo_end_team2']
    with open('outputs/games_output.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(games)

def export_teams (teams):
    field_names = ['short_name','full_name','division','mascot','conference','elo','location','eligible','twitter','color','ret_2023','ret_2022','ret_2021']
    with open('outputs/teams_output.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(teams)
    json_object_teams = json.dumps(teams, indent = 4)
    with open("outputs/teams.json", "w") as outfile:
        outfile.write(json_object_teams)

def export_tracking (tracking):
    df_track = pd.DataFrame(tracking)
    df_track.rename(columns=df_track.iloc[0]).drop(df_track.index[0])
    df_track.transpose()
    df_track.to_csv('outputs/tracking.csv',index=False)


def season_stats(year):
    teams = []
    with open(f"inputs/static/VBelo - teamstats_{year}.csv", 'r') as data:
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
    with open("outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

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
                    teams[x]['points_game'] = round(teams[x]['point_diff']/teams[x]['games'],2)
                    teams[x]['points_set'] = round(teams[x]['point_diff']/(teams[x]['sets_won']+teams[x]['sets_lost']),2)

                if games[i]['t2'] == teams[x]['short_name']:
                    teams[x]['elo'] = round(float(games[i]['elo_end_team2']),2)
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
                    teams[x]['points_set'] = round(teams[x]['point_diff']/(teams[x]['sets_won']+teams[x]['sets_lost']),2)

        field_names = ['short_name', 'full_name', 'division', 'conference', 'elo', 'games', 'wins', 'losses', 'win_pct',
                       'conf_wins', 'conf_losses', 'conf_pct', 'home_wins', 'home_losses', 'home_pct', 'away_wins',
                       'away_losses', 'away_pct', 'sets_won', 'sets_lost', 'set_diff', 'points_won', 'points_lost',
                       'point_diff', 'soo', 'sos', 'cinco_wins', 'cinco_losses', 'cinco_pct', 'points_game',
                       'points_set']
        with open(f'outputs/teamstats_output_{year}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(teams)
def top25 (teams):
    df = pd.DataFrame.from_dict(teams)
    df = df.loc[df['eligible'] == '1']
    df = df.sort_values(['elo'], ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    df['elo'] = df['elo'].round(decimals = 0).astype(int)
    df.rename(columns = {'full_name':'School', 'elo':'Elo Rating'}, inplace = True)
    df.index.name = "Rank"
    rank = df[['School','Elo Rating']].head(25)

    # Table
    fig, ax = plt.subplots(dpi=200)
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    plt.title('VBelo Ranking', loc='center',pad='40',size='x-large',family='Cambria',weight='bold')
    table = ax.table(cellText=rank.values, colLabels=rank.columns, loc='center',rowLabels=rank.index)
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(rank.columns))))
    plt.text(0,-0.072,f"Games through: {last_date}",ha='center',size='small',family='Cambria')
    cells = table.properties()["celld"]
    for i in range(0, 26):
        cells[i, 1].set_text_props(ha="center")

    #display table
    fig.tight_layout()
    plt.savefig("outputs/elo_top_25.jpg")
    plt.show()

season(30,-1,'2020')
season_stats(year_stats)
top25(teams)
