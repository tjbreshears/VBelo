# NCAA Men's Volleyball Elo
*Game Data through 03/22/2021*

*Recently added: margin-of-victory, Carolinas Conference games*

![Rankings throuhg 3/22/21](/images/elo032221.png)

## The Project
Volleyball, a much beloved sport, is significantly lacking in the category of advanced statistics. This is an attempt to help bring the widely used elo rating system into men's collegiate volleyball.

Currently, only wins and losses are taken into account. Margin of victory (sets and points) is a future addition to the model as well as home court advantage.

Huge thanks to Jonathan Bates [@mpsf_bias](http://www.twitter.com/mpsf_bias) for contributing thoughts and tons of data.

## The Data
***Always looking for more data. Let me know if you are interested in helping with data collection.***

**[2021 Games](inputs/games_2021.csv)** - A list of games where at least one team is having their elo ["tracked."](#considerations)
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

**[Teams List](inputs/teams.csv)** - A complete list of D-I, D-II, and D-III men's volleyball programs. Select NAIA schools added if they play a ["tracked"](#considerations) match.
|Field|Description|
| ----------- | ----------- |
|short_name|School name used in games spreadsheet.|
|full_name|Full name of the school, in case it is needed or unclear.|
|division|D-I, D-II, D-III, or NAIA.|
|mascot|...This data could be helpful.|
|conference|For NCAA teams, the conference that they play men's volleyball in. For NAIA, value = NAIA.|
|elo| Placeholder for elo rating as matches are played. In output, this is where elo is stored.|
|tracking|If team has its games added to games spreadsheet, value = 1.|

## The Details
### What teams are in the model?
The goal is to include all NCAA D-I and D-II teams since they are all competing for the same national championship. This includes the following conferences:
* Big West
* Carolinas Conference
* EIVA
* MIVA
* MPSF

* Independent Teams - Data Collection in progress

*Harvard, Princeton, the SIAC conference are not playing any games in the 2021 season and are, thus, not included. Technically, KSU played a match but it was exhibition.

### What about D-III and NAIA teams?
Sadly, there is not enough resources to collect all of the data needed to include D-III and NAIA. (If someone wants to collect that data, they could use this same code, though.)

Since D-I and D-II teams often play non-conference games against D-III and NAIA opponents, they have a static role in the model (i.e. their elo is always the same.) Thanks to volleyball stat nerd Jonathan, the average winning percentage of these teams vs. D-I and D-II programs was used to get their static elo ratings.
* D-III = 1419
* NAIA = 1373

### What about margin of victory?
Currently, sets won/lost are taken into account. Eventually, points will be added too.
