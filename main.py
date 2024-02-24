from dotenv import dotenv_values
from collect.espn_connector import EspnConnector
from collect.fangraphs_connector import return_fg_df
import polars as pl
from collect.fangraphs_requests import fangraphs_request
import re

# grab env file values
env_config = dotenv_values('.env')

# instantiate connector object
oConnector: object = EspnConnector(env_config)
# get owners and roster dfs
owners: pl.DataFrame = oConnector.build_team_owner_list()
rosters: pl.DataFrame = oConnector.build_fantasy_rosters()

# merge data sets
rosters_owners = rosters.join(owners, how='left', left_on='fantasy_team_id', right_on='team_id').select([
    'espn_player_id', 'player_first', 'player_last', 'keeper_current', 'keeper_prior', 'positions', 'fantasy_team_id',
    'abbrev', 'team_name', 'owner_first', 'owner_last', 'player_full'])

# write output csv file for espn rosters
rosters_owners.write_csv('output/espn_rosters.csv')

####  -----  HISTORICAL DATA  -----  ####
historical_23_pitcher: pl.DataFrame = return_fg_df(fangraphs_request['pitching_twenty_three'])
historical_23_pitcher.columns = [c + '_2023' if c not in ['PlayerName', 'fg_playerid', 'Throws'] else c for c in
                                 historical_23_pitcher.columns]
historical_22_pitcher: pl.DataFrame = return_fg_df(fangraphs_request['pitching_twenty_two'])
historical_22_pitcher.columns = [c + '_2022' if c not in ['PlayerName', 'fg_playerid', 'Throws'] else c for c in
                                 historical_22_pitcher.columns]
historical_21_pitcher: pl.DataFrame = return_fg_df(fangraphs_request['pitching_twenty_one'])
historical_21_pitcher.columns = [c + '_2021' if c not in ['PlayerName', 'fg_playerid', 'Throws'] else c for c in
                                 historical_21_pitcher.columns]

historical_23_hitter: pl.DataFrame = return_fg_df(fangraphs_request['batting_twenty_three'])
historical_23_hitter.columns = [c + '_2023' if c not in ['PlayerName', 'fg_playerid', 'Bats'] else c for c in
                                historical_23_hitter.columns]
historical_22_hitter: pl.DataFrame = return_fg_df(fangraphs_request['batting_twenty_two'])
historical_22_hitter.columns = [c + '_2022' if c not in ['PlayerName', 'fg_playerid', 'Bats'] else c for c in
                                historical_22_hitter.columns]
historical_21_hitter: pl.DataFrame = return_fg_df(fangraphs_request['batting_twenty_one'])
historical_21_hitter.columns = [c + '_2021' if c not in ['PlayerName', 'fg_playerid', 'Bats'] else c for c in
                                historical_21_hitter.columns]

# --- merge sets ---- #
# historical pitcher
prior_three_years_pitcher: pl.DataFrame = historical_23_pitcher.join(historical_22_pitcher, how='left',
                                                                     on=['fg_playerid', 'PlayerName', 'Throws'])
prior_three_years_pitcher: pl.DataFrame = prior_three_years_pitcher.join(historical_21_pitcher, how='left',
                                                                         on=['fg_playerid', 'PlayerName', 'Throws'])
# historical hitter
prior_three_years_hitter: pl.DataFrame = historical_23_hitter.join(historical_22_hitter, how='left',
                                                                   on=['fg_playerid', 'PlayerName', 'Bats'])
prior_three_years_hitter: pl.DataFrame = prior_three_years_hitter.join(historical_21_hitter, how='left',
                                                                       on=['fg_playerid', 'PlayerName', 'Bats'])

# --- merge in espn rosters ---- #
pitcher_history_rosters: pl.DataFrame = prior_three_years_pitcher.join(rosters_owners, how='left', left_on='PlayerName',
                                                                       right_on='player_full')
hitter_history_rosters: pl.DataFrame = prior_three_years_hitter.join(rosters_owners, how='left', left_on='PlayerName',
                                                                     right_on='player_full')

# --- Auction Dollar Projections --- #
def return_merged_table(table_list: list):
    projection_table: pl.DataFrame = pl.DataFrame()
    for projection in table_list:
        suffix = '_' + re.match(r'([a-zA-Z]+)_', projection).group(1)
        new_projection: pl.DataFrame = return_fg_df(fangraphs_request[projection])
        if projection_table.is_empty():
            projection_table = new_projection
        else:
            projection_table = projection_table.join(new_projection, how='left', on=['fg_playerid'],
                                                                   suffix=suffix)
    return projection_table

hitter_projections: list = ['steamer_hitter', 'atc_hitter', 'batx_hitter']
pitcher_projections: list = ['steamer_pitcher', 'atc_pitcher', 'batx_pitcher']

hitter_projection_table = return_merged_table(hitter_projections)
pitcher_projection_table = return_merged_table(pitcher_projections)

print(hitter_projection_table.head())
print(pitcher_projection_table.head())