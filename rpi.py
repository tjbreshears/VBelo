import csv
import time
import config


def winpercentage(year, main, parent):
    teams = []
    with open("inputs/VBelo - teams.csv", 'r') as data:
        for line in csv.DictReader(data):
            teams.append(line)

    games = []
    with open("outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    # find all eligible matches
    matches = []
    for game in games:
        if game['season'] == year and game['r_t1'] != '' and game['p'] == '0':
            t1 = game['t1']
            t2 = game['t2']
            t1e = 'bad'
            t2e = 'bad'

            for team in teams:
                if team['short_name'] == t1 and team['eligible'] == '1':
                    t1e = 'good'
            for team in teams:
                if team['short_name'] == t2 and team['eligible'] == '1':
                    t2e = 'good'
            if t1e == 'good' and t2e == 'good':
                matches.append(game)

    main_win = 0
    main_loss = 0
    for match in matches:
        if match['t1'] == main and match['t2'] != parent:
            if match['r_t1'] == '1':
                main_win += 1
            elif match['r_t1'] == '0':
                main_loss += 1
        if match['t2'] == main and match['t1'] != parent:
            if match['r_t2'] == '1':
                main_win += 1
            elif match['r_t2'] == '0':
                main_loss += 1
    if main_win + main_loss > 0:
        main_wp = main_win/(main_win + main_loss)
    else:
        main_wp = 0
    print(main, main_win, main_loss, main_wp)


def rpi(year):
    teams = []
    with open("inputs/VBelo - teams.csv", 'r') as data:
        for line in csv.DictReader(data):
            teams.append(line)

    games = []
    with open("outputs/games_output.csv", 'r') as data:
        for line in csv.DictReader(data):
            games.append(line)

    # find all eligible matches
    matches = []
    for game in games:
        if game['season'] == year and game['r_t1'] != '':
            t1 = game['t1']
            t2 = game['t2']
            t1e = 'bad'
            t2e = 'bad'

            for team in teams:
                if team['short_name'] == t1 and team['eligible'] == '1':
                    t1e = 'good'
            for team in teams:
                if team['short_name'] == t2 and team['eligible'] == '1':
                    t2e = 'good'
            if t1e == 'good' and t2e == 'good':
                matches.append(game)

    rpi_list = []

    # Go through every eligible team
    for team in teams:
        if team['eligible'] == '1':
            focus_team = team['short_name']
            focus_name = team['full_name']
            focus_win = 0
            focus_loss = 0

            # find winning percentage
            for match in matches:
                if match['t1'] == focus_team:
                    if match['r_t1'] == '1':
                        focus_win += 1
                    elif match['r_t1'] == '0':
                        focus_loss += 1
                elif match['t2'] == focus_team:
                    if match['r_t2'] == '1':
                        focus_win += 1
                    elif match['r_t2'] == '0':
                        focus_loss += 1

            # find opponent winning percentage
            opp_list = []

            for match in matches:
                opp_win = 0
                opp_loss = 0
                if match['t1'] == focus_team:
                    opp = match['t2']
                    for match2 in matches:
                        if match2['t1'] == opp and match2['t2'] != focus_team:
                            if match2['r_t1'] == '1':
                                opp_win += 1
                            elif match2['r_t1'] == '0':
                                opp_loss += 1
                        elif match2['t2'] == opp and match2['t1'] != focus_team:
                            if match2['r_t2'] == '1':
                                opp_win += 1
                            elif match2['r_t2'] == '0':
                                opp_loss += 1
                    if opp_win + opp_loss > 0:
                        single_owp = opp_win / (opp_win + opp_loss)
                    else:
                        single_owp = 0
                    opp_list.append(single_owp)
                elif match['t2'] == focus_team:
                    opp = match['t1']
                    for match2 in matches:
                        if match2['t1'] == opp and match2['t2'] != focus_team:
                            if match2['r_t1'] == '1':
                                opp_win += 1
                            elif match2['r_t1'] == '0':
                                opp_loss += 1
                        elif match2['t2'] == opp and match2['t1'] != focus_team:
                            if match2['r_t2'] == '1':
                                opp_win += 1
                            elif match2['r_t2'] == '0':
                                opp_loss += 1
                    if opp_win + opp_loss > 0:
                        single_owp = opp_win / (opp_win + opp_loss)
                    else:
                        single_owp = 0
                    opp_list.append(single_owp)

            # find opponent's opponent winning percentage
            oowp_list = []

            for match in matches:

                # case where focus team is team 1
                if match['t1'] == focus_team:
                    opponent = match['t2']
                    owp2_list = []
                    for match2 in matches:
                        if match2['t1'] == opponent:
                            opponent2 = match2['t2']
                            opponent2_win = 0
                            opponent2_loss = 0
                            for match3 in matches:
                                if match3['t1'] == opponent2 and match3['t2'] != opponent:
                                    if match3['r_t1'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t1'] == '0':
                                        opponent2_loss += 1
                                elif match3['t2'] == opponent2 and match3['t1'] != opponent:
                                    if match3['r_t2'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t2'] == '0':
                                        opponent2_loss += 1
                            if opponent2_win + opponent2_loss > 0:
                                owp_entry2 = opponent2_win / (opponent2_win + opponent2_loss)
                            else:
                                owp_entry2 = 0
                            owp2_list.append(owp_entry2)

                        elif match2['t2'] == opponent:
                            opponent2 = match2['t1']
                            opponent2_win = 0
                            opponent2_loss = 0
                            for match3 in matches:
                                if match3['t1'] == opponent2 and match3['t2'] != opponent:
                                    if match3['r_t1'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t1'] == '0':
                                        opponent2_loss += 1
                                elif match3['t2'] == opponent2 and match3['t1'] != opponent:
                                    if match3['r_t2'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t2'] == '0':
                                        opponent2_loss += 1
                            if opponent2_win + opponent2_loss > 0:
                                owp_entry2 = opponent2_win / (opponent2_win + opponent2_loss)
                            else:
                                owp_entry2 = 0
                            owp2_list.append(owp_entry2)

                    if len(owp2_list) > 0:
                        oowp_entry = sum(owp2_list) / len(owp2_list)
                    else:
                        oowp_entry = 0
                    oowp_list.append(oowp_entry)

                # case where focus team is team 2
                elif match['t2'] == focus_team:
                    opponent = match['t1']
                    owp2_list = []
                    for match2 in matches:
                        if match2['t1'] == opponent:
                            opponent2 = match2['t2']
                            opponent2_win = 0
                            opponent2_loss = 0
                            for match3 in matches:
                                if match3['t1'] == opponent2 and match3['t2'] != opponent:
                                    if match3['r_t1'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t1'] == '0':
                                        opponent2_loss += 1
                                elif match3['t2'] == opponent2 and match3['t1'] != opponent:
                                    if match3['r_t2'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t2'] == '0':
                                        opponent2_loss += 1
                            if opponent2_win + opponent2_loss > 0:
                                owp_entry2 = opponent2_win / (opponent2_win + opponent2_loss)
                            else:
                                owp_entry2 = 0
                            owp2_list.append(owp_entry2)

                        elif match2['t2'] == opponent:
                            opponent2 = match2['t1']
                            opponent2_win = 0
                            opponent2_loss = 0
                            for match3 in matches:
                                if match3['t1'] == opponent2 and match3['t2'] != opponent:
                                    if match3['r_t1'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t1'] == '0':
                                        opponent2_loss += 1
                                elif match3['t2'] == opponent2 and match3['t1'] != opponent:
                                    if match3['r_t2'] == '1':
                                        opponent2_win += 1
                                    elif match3['r_t2'] == '0':
                                        opponent2_loss += 1
                            if opponent2_win + opponent2_loss > 0:
                                owp_entry2 = opponent2_win / (opponent2_win + opponent2_loss)
                            else:
                                owp_entry2 = 0
                            owp2_list.append(owp_entry2)

                    if len(owp2_list) > 0:
                        oowp_entry = sum(owp2_list) / len(owp2_list)
                    else:
                        oowp_entry = 0
                    oowp_list.append(oowp_entry)

            # stats of eligible teams
            if focus_win + focus_loss > 0:
                wp = focus_win / (focus_win + focus_loss)
            else:
                wp = 0
            if len(opp_list) > 0:
                owp = sum(opp_list)/len(opp_list)
            else:
                owp = 0
            if len(oowp_list) > 0:
                oowp = sum(oowp_list) / len(oowp_list)
            else:
                oowp = 0
            total = (wp * 0.25) + (owp * 0.50) + (oowp * 0.25)
            entry = {'team': focus_name, 'wp': wp, 'owp': owp, 'oowp': oowp, 'rpi': total}
            rpi_list.append(entry)

    field_names = ['team', 'wp', 'owp', 'oowp', 'rpi']
    with open(f'outputs/rpi_{year}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rpi_list)


if __name__ == '__main__':
    start_time = time.time()
    rpi(config.current_year)
    print("--- %s seconds ---" % (time.time() - start_time))
