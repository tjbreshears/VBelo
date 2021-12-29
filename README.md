# VBelo - NCAA Men's Volleyball Elo
*Game Data through 2021 season*

*Recently added: Added distance traveled adjustment*

![Rankings through 5/8/21](/images/elo050821.png)

## The Project
Volleyball, a much beloved sport, is significantly lacking in the category of advanced statistics. This is an attempt to help bring the widely used elo rating system into men's collegiate volleyball.

The main input for this elo model is wins/losses, but sets won, home court advantage, and distance traveled disadvantage is also taken into account. (Points data is in the data set, but currently not used in the elo calculation.)

Huge thanks to Jonathan Bates [@mpsf_bias](http://www.twitter.com/mpsf_bias) for contributing thoughts and tons of data.

## The Data
***Always looking for more data. Let me know if you are interested in helping with data collection.***

**[2021 Games](inputs/games.csv)** - A list of games where at least one team is eligible to compete for the NCAA D-I/II Championship.
|Field|Description|
| ----------- | ----------- |
|date|Date the game was played.|
|season|Calendar year season for the game (for future data).|
|home|Displays home teams. If neutral court, field is blank.|
|neutral|If played on neutral court, value = 1.|
|playoff|If game is a playoff game, value = 1.|
|team1|Away team. If neutral court, team with "short_name" that comes alphabetically first.|
|team2|Home team. If neutral court, team with "short_name" that comes alphabetically second.|
|result_team#|Win = 1. Loss = 0.|
|sets_team#|Number of sets team# won.|
|points_team#|Number of total points team# scored in all sets.|
|elo_start_team#|The elo rating at the beginning of the match for team#.|
|probability_team#|Probability that team# will will the game given both teams beginning elo rating.|
|elo_end_team#|The elo rating at the end of the match after match results are complete.|

**[Teams List](inputs/teams.csv)** - A complete list of D-I, D-II, and D-III men's volleyball programs. Select NAIA and NCCAA schools added if they play a Championship eligible team.
|Field|Description|
| ----------- | ----------- |
|short_name|School name used in games spreadsheet.|
|full_name|Full name of the school, in case it is needed or unclear.|
|division|D-I, D-II, D-III, NAIA, or NCCAA.|
|mascot|...This data could be helpful.|
|conference|For NCAA teams, the conference that they play men's volleyball in. For NAIA, value = NAIA.|
|elo| Placeholder for elo rating as matches are played. In output, this is where elo is stored.|
|location|Longitude and latitude for home games.|
|eligible|Teams that compete for the D-I/II championship and are therefore have their elo tracked, value = 1.|

## The Details
### What teams are in the model?
The goal is to include all NCAA D-I and D-II teams since they are all competing for the same national championship. This includes the following conferences:
* Big West
* Carolinas Conference
* EIVA
* MIVA
* MPSF
* Independent Teams

### What about D-III, NAIA, and NCCAA teams?
Sadly, there is not enough resources to collect all of the data needed to include all collegiate men's volleyball. (If someone wants to collect that data, they could use this same code, though.)

Since D-I and D-II teams often play non-conference games against D-III, NAIA, or NCCAA opponents, they have a static role in the model (i.e. their elo is always the same.) Thanks to volleyball stat nerd Jonathan, the average winning percentage of these teams vs. D-I and D-II programs was used to get their static elo ratings.
* D-III = 1419
* NAIA/NCCAA = 1373

### What about margin of victory?
Currently, sets won/lost are taken into account. Eventually, points will be added too.

### What about home court advantage?
There is a seemingly significant advantage to playing at home in NCAA Men's Volleyball. Between 2015 and 2020, home teams won a little over 63% of the time. \([All credit to this goes to Jonathan Bates.](https://www.offtheblockblog.com/2021/04/data-analysis-home-court-not-as-important-during-2021-season/)\) Since 2021 has seen a slight decrease in home court advantage, the adjustment in the model for being the home team is equal to 70 elo points. This is equivalent to about a 10% advantage. While this is below the "actual" home court advantage, this leaves room for other factors, such as travel.

### What about distance traveled?
Traveling is hard, so I want the model to reflect that. By looking at mean squared errors, and some trial and error, the current penalty for distance traveled is as follows:
* -1 elo for every 250 miles traveled to the venue
* There is a max penalty of -25 elo (no one has reached this yet)
* For neutral site games, both teams could get this travel penalty (depending on how far the match is from both schools)

### What about players graduating and year-to-year changes?
Obviously, no program has the exact same roster two years in a row. To help adjust for graduates and/or transfers (and potentially elo inflation), at the beginning of each season, every team will have their elo reverted by 1/3 to 1500 (the average elo).

### What is the K value?
It is currently 24. That was the best value to optimize the mean squared error (~0.16). As more data is collected, this will be revisited.
