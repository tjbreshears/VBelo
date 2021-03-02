import csv

teams = []

with open("data/ncaa_d1_mens_teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)

#set initial elo for every team to 1200
for i in range(len(teams)):
    teams[i]["elo"] = 1200

print(teams)

#-------------------------
#from elo_test.py
import math

#Teams in game
#eventually this will move to spreadsheet
team1 = 'UH'
team2 = 'BYU'

# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


def eloRating(t1, t2, d):
    K = 30

    for i in range(len(teams)):
        if t1 == teams[i]['short_name']:
            r1 = teams[i]['elo']
    for i in range(len(teams)):
        if t2 == teams[i]['short_name']:
            r2 = teams[i]['elo']

    p1 = probability(r2, r1)
    p2 = probability(r1, r2)

    if (d == 1):
        r1 = r1 + K * (1 - p1)
        r2 = r2 + K * (0 - p2)

    else:
        r1 = r1 + K * (0 - p1)
        r2 = r2 + K * (1 - p2)
    print("Updated Ratings:")
    print(d)
    print(f"{t1}:", round(r1, 6)," t2 =", round(r2, 6))
    for i in range(len(teams)):
        if t1 == teams[i]['short_name']:
            teams[i]['elo'] = r1
    for i in range(len(teams)):
        if t2 == teams[i]['short_name']:
            teams[i]['elo'] = r2



eloRating(team1, team2, 1)
print(teams)
