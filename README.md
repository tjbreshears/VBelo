# NCAA Men's Volleyball Elo
*Game Data through 03/04/2021*

## The Project
Volleyball, a much beloved sport, is significantly lacking in the category of advanced statistics. This is an attempt to help bring the widely used elo rating system into men's collediate volleyball.

Currently, only wins and losses are taken into account. Margin of victory (sets and points) is a future addition to the model as well as home court advantage.

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

## Considerations
### Whose games are "tracked"/ who gets a dynamic elo rating?
* Big West
* EIVA
* MIVA
* MPSF

These conferences are predominantly D-I programs. The D-II schools that play in these conferences have similar schedule strengths so their games are also tracked.

### Whose games are not "tracked/ who gets a constant elo rating?
* Carolinas Conference = [1200](calibration/non_tracking_base_elo.py)
* SIAC = [1200](calibration/non_tracking_base_elo.py)
* Independent Teams = [1200](calibration/non_tracking_base_elo.py)
* NCAA D-III = 1100 (splitting the difference between the above and below groups)
* NAIA = 1000 (should be [988.50](calibration/naia_base_elo.py) to give 5% chance at beating average team)
