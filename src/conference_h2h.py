import csv

games = []
with open("outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)

h2h = []
with open("inputs/VBelo - conference_h2h.csv", 'r') as data:
    for line in csv.DictReader(data):
        h2h.append(line)

teams = []
with open("inputs/VBelo - teams.csv", 'r') as data:
    for line in csv.DictReader(data):
        teams.append(line)
for i in range(len(teams)):
    teams[i]['elo'] = int(teams[i]['elo'])

not_tracked = ['D-III','NAIA','NCCAA','n/a']

def ooc (year):
    for i in range(len(games)):
        if games[i]['season'] == year and games[i]['r_t1'] != '':
            t1_c = ''
            t2_c = ''
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    t1_c = teams[x]['conference']
                if games[i]['t2'] == teams[x]['short_name']:
                    t2_c = teams[x]['conference']
            if t1_c not in not_tracked and t2_c not in not_tracked and t1_c != t2_c:
#                print(t1_c,t2_c)
                for y in range(len(h2h)):
                    if games[i]['r_t1'] == '1' and h2h[y]['conference'] == t1_c:
                        h2h[y][t2_c] = int(h2h[y][t2_c]) + 1
                    if games[i]['r_t2'] == '1' and h2h[y]['conference'] == t2_c:
                        h2h[y][t1_c] = int(h2h[y][t1_c]) + 1

def export_h2h (h2h):
    field_names = ['conference','Big West','Carolinas','EIVA','Independent','MIVA','MPSF','SIAC']
    with open('outputs/h2h.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(h2h)

ooc('2022')
export_h2h(h2h)
