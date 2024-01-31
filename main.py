from dotenv import dotenv_values
from collect.espn_connector import EspnConnector
import polars as pl

# grab env file values
env_config = dotenv_values('.env')

# instantiate connector object
oConnector: object = EspnConnector(env_config)
# get owners and roster dfs
owners: pl.DataFrame = oConnector.build_team_owner_list()
rosters: pl.DataFrame = oConnector.build_fantasy_rosters()

# merge data sets
rosters_owners = rosters.join(owners, how='left', left_on='fantasy_team_id', right_on='team_id').select([
    'espn_player_id', 'player_first', 'player_last', 'keeper_current', 'keeper_prior', 'positions', 'fantasy_team_id', 'abbrev', 'team_name', 'owner_first', 'owner_last', 'player_full'])

# write output csv file
rosters_owners.write_csv('output/espn_rosters.csv')
