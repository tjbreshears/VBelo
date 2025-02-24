import csv
import config

games = []
with open("../../outputs/games_output.csv", 'r') as data:
    for line in csv.DictReader(data):
        games.append(line)


def first_set():
    win3 = 0
    win4 = 0
    win5 = 0
    lose4 = 0
    lose5 = 0

    for i in range(len(games)):
        if games[i]['season'] in ['2022', '2023'] and games[i]['s1_t1'] != '' \
                and int(games[i]['s1_t1']) > int(games[i]['s1_t2']):
            if int(games[i]['s_t1']) + int(games[i]['s_t2']) == 3 and games[i]['r_t1'] == '1':
                win3 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 4 and games[i]['r_t1'] == '1':
                win4 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5 and games[i]['r_t1'] == '1':
                win5 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 4 and games[i]['r_t1'] == '0':
                lose4 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5 and games[i]['r_t1'] == '0':
                lose5 += 1

        if games[i]['season'] in ['2022', '2023', '2024'] and games[i]['s1_t1'] != '' \
                and int(games[i]['s1_t2']) > int(games[i]['s1_t1']):
            if int(games[i]['s_t1']) + int(games[i]['s_t2']) == 3 and games[i]['r_t2'] == '1':
                win3 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 4 and games[i]['r_t2'] == '1':
                win4 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5 and games[i]['r_t2'] == '1':
                win5 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 4 and games[i]['r_t2'] == '0':
                lose4 += 1
            elif int(games[i]['s_t1']) + int(games[i]['s_t2']) == 5 and games[i]['r_t2'] == '0':
                lose5 += 1

    print(win3)
    print(win4)
    print(win5)
    print(lose4)
    print(lose5)


first_set()
