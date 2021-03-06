import csv

def export_teams (teams):
    field_names = ['short_name','full_name','division','mascot','conference','elo','tracking']
    with open('outputs/teams_ouput.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(teams)

def export_games (games):
    field_names = ['date','season','home','neutral','playoff','team1','team2','result_team1','result_team2','sets_team1','sets_team2','points_team1','points_team2','elo_start_team1','elo_start_team2','probability_team1','probability_team2','elo_end_team1','elo_end_team2']
    with open('outputs/games_2021_ouput.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(games)
