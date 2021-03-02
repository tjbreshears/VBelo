import csv

teams = []

with open("data/ncaa_d1_mens_teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)

#set initial elo for every team to 1200
for i in range(len(teams)):
    teams[i]["elo"] = 1200

print(teams)
