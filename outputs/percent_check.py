import csv

games = []
with open("outputs/games_2021_output", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)



z1_w = 0
z1_t = 0
z2_w = 0
z2_t = 0
z3_w = 0
z3_t = 0
z4_w = 0
z4_t = 0
z5_w = 0
z5_t = 0
z6_w = 0
z6_t = 0
z7_w = 0
z7_t = 0
z8_w = 0
z8_t = 0
z9_w = 0
z9_t = 0
z10_w = 0
z10_t = 0

for i in range(len(games)):
    if 0.0 <= float(games[i]['probability_team1']) < 0.30 and games[i]['result_team1'] != '':
        z1_w += int(games[i]['result_team1'])
        z1_t += 1
    elif 0.30 <= float(games[i]['probability_team1']) < 0.35 and games[i]['result_team1'] != '':
        z2_w += int(games[i]['result_team1'])
        z2_t += 1
    elif 0.35 <= float(games[i]['probability_team1']) < 0.40 and games[i]['result_team1'] != '':
        z3_w += int(games[i]['result_team1'])
        z3_t += 1
    elif 0.40 <= float(games[i]['probability_team1']) < 0.45 and games[i]['result_team1'] != '':
        z4_w += int(games[i]['result_team1'])
        z4_t += 1
    elif 0.45 <= float(games[i]['probability_team1']) < 0.50 and games[i]['result_team1'] != '':
        z5_w += int(games[i]['result_team1'])
        z5_t += 1
    elif 0.50 <= float(games[i]['probability_team1']) < 0.55 and games[i]['result_team1'] != '':
        z6_w += int(games[i]['result_team1'])
        z6_t += 1
    elif 0.55 <= float(games[i]['probability_team1']) < 0.60 and games[i]['result_team1'] != '':
        z7_w += int(games[i]['result_team1'])
        z7_t += 1
    elif 0.60 <= float(games[i]['probability_team1']) < 0.65 and games[i]['result_team1'] != '':
        z8_w += int(games[i]['result_team1'])
        z8_t += 1
    elif 0.65 <= float(games[i]['probability_team1']) < 0.70 and games[i]['result_team1'] != '':
        z9_w += int(games[i]['result_team1'])
        z9_t += 1
    elif 0.70 <= float(games[i]['probability_team1']) < 1 and games[i]['result_team1'] != '':
        z10_w += int(games[i]['result_team1'])
        z10_t += 1

print(f"0-30%: Wins-{z1_w}, Games-{z1_t}, Percent-{z1_w/z1_t}")
print(f"30-35%: Wins-{z2_w}, Games-{z2_t}, Percent-{z2_w/z2_t}")
print(f"35-40%: Wins-{z3_w}, Games-{z3_t}, Percent-{z3_w/z3_t}")
print(f"40-45%: Wins-{z4_w}, Games-{z4_t}, Percent-{z4_w/z4_t}")
print(f"45-50%: Wins-{z5_w}, Games-{z5_t}, Percent-{z5_w/z5_t}")
print(f"50-55%: Wins-{z6_w}, Games-{z6_t}, Percent-{z6_w/z6_t}")
print(f"55-60%: Wins-{z7_w}, Games-{z7_t}, Percent-{z7_w/z7_t}")
print(f"60-65%: Wins-{z8_w}, Games-{z8_t}, Percent-{z8_w/z8_t}")
print(f"65-70%: Wins-{z9_w}, Games-{z9_t}, Percent-{z9_w/z9_t}")
print(f"70-100%: Wins-{z10_w}, Games-{z10_t}, Percent-{z10_w/z10_t}")
