import polars as pl
import requests


class EspnConnector:
    def __init__(self, env_config: dict):
        self.api_url = env_config['ESPN_API_URL']
        self.swid = env_config['swid']
        self.espn_s2 = env_config['espn_s2']

    def make_positions(self, position_numbers: list) -> str:
        """
        takes a list of espn encoded positions and converts them to a string list of their equivalent abbreviations
        """
        eligibleSlotsMap: dict = {0: 'c', 1: '1b', 2: '2b', 3: '3b', 4: 'ss', 5: 'of', 12: 'dh', 14: 'sp', 15: 'rp'}
        positions: str = ''
        for eligible_slot in position_numbers:
            if eligible_slot in eligibleSlotsMap.keys():
                positions = positions + eligibleSlotsMap[eligible_slot] + ', '
        # slice last comma and space off the positions list when returning the value
        return positions[:-2]

    def get_espn_data(self, url, view: str, headers: dict = None) -> object:
        """
        calls the espn API with our stored credentials and returns different data based upon the view we ask the API for
        """
        response = requests.get(url, cookies={'swid': self.swid, 'espn_s2': self.espn_s2}, params={'view': view},
                                headers=headers)
        return response.json()

    def build_fantasy_rosters(self) -> pl.DataFrame:
        """
        Builds a data frame of all rostered fantasy players and also calculates their keeper value for the next season
        """
        rosters_json: object = self.get_espn_data(self.api_url, 'mRoster')
        fantasy_rosters: pl.DataFrame = pl.DataFrame()
        # loop over every team and every player to extract the key information in the json file
        for team in rosters_json['teams']:
            for player in team['roster']['entries']:
                positions: str = self.make_positions(player['playerPoolEntry']['player']['eligibleSlots'])
                if player['playerPoolEntry']['keeperValue'] == 0:
                    keeper_current: int = 1
                else:
                    keeper_current = player['playerPoolEntry']['keeperValue'] + 5
                player_row = pl.DataFrame({
                    'espn_player_id': player['playerPoolEntry']['id'],
                    'keeper_prior': player['playerPoolEntry']['keeperValue'],
                    'fantasy_team_id': player['playerPoolEntry']['onTeamId'],
                    'player_first': player['playerPoolEntry']['player']['firstName'],
                    'player_last': player['playerPoolEntry']['player']['lastName'],
                    'player_full': player['playerPoolEntry']['player']['fullName'],
                    'positions': positions,
                    'keeper_current': keeper_current
                })
                fantasy_rosters = pl.concat([fantasy_rosters, player_row])
        return fantasy_rosters

    def build_team_owner_list(self) -> pl.DataFrame:
        """
        Builds a data frame of team owners
        """
        owners_json: object = self.get_espn_data(self.api_url, 'mTeam')
        owners_df: pl.DataFrame = pl.DataFrame()
        for owner in owners_json['members']:
            owner_row: pl.DataFrame = pl.DataFrame(
                {'owner_first': owner['firstName'], 'owner_last': owner['lastName'], 'owner_id': owner['id']})
            owners_df = pl.concat([owners_df, owner_row])

        team_df: pl.DataFrame = pl.DataFrame()
        for team in owners_json['teams']:
            # if a team has no owner, loop will throw an error. The try-except block catches and passes None for owner
            try:
                team_row: pl.DataFrame = pl.DataFrame(
                    {'abbrev': team['abbrev'], 'team_name': team['name'], 'team_id': team['id'],
                     'owner_id': team['primaryOwner']})
            except KeyError:
                team_row: pl.DataFrame = pl.DataFrame(
                    {'abbrev': team['abbrev'], 'team_name': team['name'], 'team_id': team['id'], 'owner_id': None})
            team_df = pl.concat([team_df, team_row])

        owners_teams = team_df.join(owners_df, how='left', on='owner_id').drop('owner_id')
        return owners_teams

    def build_draft_results(self, year: str) -> pl.DataFrame:
        draft_api_url: str = self.api_url.replace('2024', year)
        draft_json: dict = self.get_espn_data(draft_api_url, 'mDraftDetail')
        picks: list = draft_json['draftDetail']['picks']
        picks_df: pl.DataFrame = pl.DataFrame(picks)
        return picks_df.select(
            ['playerId', 'keeper', 'bidAmount', 'teamId', 'overallPickNumber', 'roundId', 'roundPickNumber',
             'nominatingTeamId'])

    def build_player_list(self, year: str) -> pl.DataFrame:
        draft_api_url: str = 'https://fantasy.espn.com/apis/v3/games/flb/seasons/2023/players?scoringPeriodId=0&view=players_wl'
        # headers: str = {'x-fantasy-filter': '{"filterActive": null}',
        #                 'x-fantasy-platform': 'kona-PROD-1dc40132dc2070ef47881dc95b633e62cebc9913',
        #                 'x-fantasy-source': 'kona'
        #                 }
        headers = {
            'x - fantasy - filter': '{“filterActive”:null}',
            'x - fantasy - platform': 'kona - PROD - 1dc40132dc2070ef47881dc95b633e62cebc9913',
            'x - fantasy - source': 'kona'
        }
        response = requests.get(draft_api_url, cookies={'swid': self.swid, 'espn_s2': self.espn_s2}, headers=headers)

        print(response.json())
