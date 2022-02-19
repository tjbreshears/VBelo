import csv
import os
import sys
from datetime import datetime, timedelta
import pyperclip as pc
import time


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

def tweet(date):
    text = 'Daily #VBelo Predictions: ' + date
    for i in range(len(games)):
        if date in games[i]['date']:
            team1 = games[i]['t1']
            team1p = round(float(games[i]['probability_team1'])*100)
            team2 = games[i]['t2']
            team2p = round(float(games[i]['probability_team2'])*100)
            for x in range(len(teams)):
                if games[i]['t1'] == teams[x]['short_name']:
                    team1 = teams[x]['twitter']
                if games[i]['t2'] == teams[x]['short_name']:
                    team2 = teams[x]['twitter']
            text += (f'\n{team1} ({team1p}%) vs {team2} ({team2p}%)')
    print('\n\n' + text + '\n\n')
    pc.copy(text)

def eod(date):
    intro = 'Daily #VBelo Recap: ' + date
    count = 0
    sets = 0
    points = 0
    diff = 0
    cinco = 0
    home_w = 0
    upsets = 0
    for i in range(len(games)):
        if date in games[i]['date']:
            count += 1
            sets = sets + int(games[i]['s_t1']) + int(games[i]['s_t2'])
            points = points + int(games[i]['p_t1']) + int(games[i]['p_t2'])
            diff = diff + abs(int(games[i]['p_t1'])-int(games[i]['p_t2']))
            if games[i]['s5_t1'] != '':
                cinco += 1
            if games[i]['home'] == games[i]['t2'] and games[i]['r_t2'] == '1':
                home_w += 1
            if games[i]['r_t1'] == '1' and float(games[i]['probability_team1']) < 0.3:
                upsets += 1
            if games[i]['r_t2'] == '1' and float(games[i]['probability_team2']) < 0.3:
                upsets += 1
    text = intro + f'''\nGames: {count}
Total Points: {points}
Sets/game: {round(sets/count,2)}
Average Set Differential: {round(diff/sets,2)} points
Home Win Pct: {round(home_w/count*100,2)}%
#cincosets: {cinco}'''
    print('\n\n' + text + '\n\n')
    pc.copy(text)

clear = lambda: os.system('cls')
clear()

menu_options = {
    1: 'Pre-Match Predictions',
    2: 'End of Day Summary',
    3: 'Exit',
}

today_date = datetime.today()
t_now = datetime.today().strftime('%#m/%#d/%Y')
t_tom = (today_date + timedelta(days=1)).strftime('%#m/%#d/%Y')
t_yes = (today_date + timedelta(days=-1)).strftime('%#m/%#d/%Y')

def print_menu():
    print("VBelo Twitter Tool")
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
     print("\n\nEnter date for daily VBelo projections (m/d/yyyy):")
     print("Shortcuts:  t-today  y-yesterday  to-tomorrow")
     date_twitter = input("\nDate: ")

     if date_twitter == 't':
         tweet(t_now)
     elif date_twitter == 'y':
         tweet(t_yes)
     elif date_twitter == 'to':
         tweet(t_tom)
     else:
         tweet(date_twitter)

def option2():
     print("\n\nEnter date for daily VBelo recap (m/d/yyyy):")
     print("Shortcuts:  t-today  y-yesterday  to-tomorrow")
     eod_twitter = input("\nDate: ")

     if eod_twitter == 't':
         eod(t_now)
     elif eod_twitter == 'y':
         eod(t_yes)
     elif eod_twitter == 'to':
         eod(t_tom)
     else:
         eod(eod_twitter)


if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            print('\n\nGoodbye!')
            time.sleep(3)
            sys.exit()
        else:
            print('Invalid option. Please enter a number between 1 and 3.')
