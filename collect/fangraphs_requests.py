import requests
import polars as pl

fangraphs_request: dict = {
    'steamer_pitcher': {
        'url': 'https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=260&mb=1&mp=20&msp=5&mrp=5&type=pit&players=&proj=steamer&split=&points=c%7C1%2C2%2C3%2C4%2C5%7C13%2C14%2C2%2C3%2C4&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C4%2C3%2C2%2C5%2C0&sort=&view=0',
        'cols_to_keep': ['PlayerName', 'playerid', 'POS', 'mERA', 'mWHIP', 'mSO', 'mSVHLD', 'PTS', 'aPOS', 'Dollars'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    },
    'steamer_hitter': {
        'url': 'https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=260&mb=1&mp=20&msp=5&mrp=5&type=bat&players=&proj=steamer&split=&points=c%7C1%2C2%2C3%2C4%2C5%7C13%2C14%2C2%2C3%2C4&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C4%2C3%2C2%2C5%2C0&sort=&view=0',
        'cols_to_keep': ['PlayerName', 'playerid', 'POS', 'mRBI', 'mR', 'mSB', 'mHR', 'mOBP', 'PTS', 'aPOS', 'Dollars'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    },
    'steamer_pitcher_stats': {
        'url': 'https://www.fangraphs.com/api/projections?pos=all&stats=pit&type=steamer',
        'cols_to_keep': ['PlayerName', 'playerid', 'GS', 'IP', 'SV', 'HLD', 'ERA', 'WHIP', 'QS', 'ER', 'BB', 'SO', 'K/9'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    },
    'steamer_hitter_stats': {
        'url': 'https://www.fangraphs.com/api/projections?pos=all&stats=bat&type=steamer',
        'cols_to_keep': ['PlayerName', 'playerid', 'G', 'PA', 'H', 'BB', 'HR', 'R', 'RBI', 'SB', 'SO',
                         'CS', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    },
    'batting_twenty_three': {
        'url': 'https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&qual=200&season=2023&season1=2023&startdate=2023-03-01&enddate=2023-11-01&month=0&hand=&team=0&pageitems=170&pagenum=1&ind=0&rost=0&players=&type=15&postseason=&sortdir=default&sortstat=pfxPace',
        'cols_to_keep': ['PlayerName', 'playerid', 'Bats', 'Age', 'G', 'PA', 'H', 'BB', 'HR', 'R', 'RBI', 'SB', 'SO',
                         'CS', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'LD%', 'GB%', 'FB%', 'HR/FB', 'Balls', 'Strikes',
                         'BB%', 'K%', 'O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Z-Contact%', 'Contact%',
                         'SwStr%', 'C+SwStr%', 'Pull%', 'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%', 'Barrel%', 'maxEV'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    },
    'pitching_twenty_three': {
        'url': 'https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=pit&lg=all&qual=40&season=2023&season1=2023&startdate=2023-03-01&enddate=2023-11-01&month=0&hand=&team=0&pageitems=130&pagenum=1&ind=0&rost=0&players=&type=8&postseason=&sortdir=default&sortstat=WAR',
        'cols_to_keep': ['PlayerName', 'playerid', 'Throws', 'Age', 'G', 'GS', 'IP', 'SV', 'HLD', 'H', 'BB', 'HR', 'ER',
                         'SO', 'BABIP', 'FIP', 'Barrel%', 'HardHit%', 'LD%', 'GB%', 'FB%', 'HR/FB', 'O-Swing%',
                         'Z-Swing%', 'O-Contact%', 'Z-Contact%', 'Contact%', 'Zone%', 'SwStr%', 'CStr%', 'C+SwStr%',
                         'Pull%', 'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%'],
        'cols_to_rename': {'playerid': 'fg_playerid'}
    }
}

addition_historical_data: list = [
    {
        'new_key': 'batting_twenty_two',
        'reference_key': 'batting_twenty_three',
        'old_string': '2023',
        'new_string': '2022'
    },
    {
        'new_key': 'batting_twenty_one',
        'reference_key': 'batting_twenty_three',
        'old_string': '2023',
        'new_string': '2021'
    },
    {
        'new_key': 'pitching_twenty_two',
        'reference_key': 'pitching_twenty_three',
        'old_string': '2023',
        'new_string': '2022'
    },
    {
        'new_key': 'pitching_twenty_one',
        'reference_key': 'pitching_twenty_three',
        'old_string': '2023',
        'new_string': '2021'
    },
    {
        'new_key': 'atc_hitter',
        'reference_key': 'steamer_hitter',
        'old_string': 'steamer',
        'new_string': 'atc'
    },
    {
        'new_key': 'atc_pitcher',
        'reference_key': 'steamer_pitcher',
        'old_string': 'steamer',
        'new_string': 'atc'
    },
    {
        'new_key': 'batx_hitter',
        'reference_key': 'steamer_hitter',
        'old_string': 'steamer',
        'new_string': 'thebatx'
    },
    {
        'new_key': 'batx_pitcher',
        'reference_key': 'steamer_pitcher',
        'old_string': 'steamer',
        'new_string': 'thebatx'
    },
    {
        'new_key': 'atc_pitcher_stats',
        'reference_key': 'steamer_pitcher_stats',
        'old_string': 'steamer',
        'new_string': 'atc'
    },
    {
        'new_key': 'batx_pitcher_stats',
        'reference_key': 'steamer_pitcher_stats',
        'old_string': 'steamer',
        'new_string': 'thebatx'
    },
    {
        'new_key': 'atc_hitter_stats',
        'reference_key': 'steamer_hitter_stats',
        'old_string': 'steamer',
        'new_string': 'atc'
    },
    {
        'new_key': 'batx_hitter_stats',
        'reference_key': 'steamer_hitter_stats',
        'old_string': 'steamer',
        'new_string': 'thebatx'
    }
]

for entry in addition_historical_data:
    fangraphs_request[entry['new_key']] = {
        'url': fangraphs_request[entry['reference_key']]['url'].replace(entry['old_string'], entry['new_string']),
        'cols_to_keep': fangraphs_request[entry['reference_key']]['cols_to_keep'],
        'cols_to_rename': fangraphs_request[entry['reference_key']]['cols_to_rename']
    }


class FangraphsUrlBuilder:
    def __init__(self):
        self.historical_url_base = 'https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&qual=200&season=2023&season1=2023&startdate=2023-03-01&enddate=2023-11-01&month=0&hand=&team=0&pageitems=30&pagenum=1&ind=0&rost=0&players=&type=15&postseason=&sortdir=default&sortstat=WAR'
        self.auction_url_base = 'https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=260&mb=1&mp=20&msp=5&mrp=5&type=pit&players=&proj=steamer&split=&points=c%7C1%2C2%2C3%2C4%2C5%7C13%2C14%2C2%2C3%2C4&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C4%2C3%2C2%2C5%2C0&sort=&view=0'
        self.projection_url_base = 'https://www.fangraphs.com/projections?pos=all&stats=bat&type=steamer'
        self.cols_to_rename = {'playerid': 'fg_playerid'}
        self.auction_cols = {
            0: ['PlayerName', 'playerid', 'POS', 'mERA', 'mWHIP', 'mSO', 'mSVHLD', 'PTS', 'aPOS',
                'Dollars'],
            1: ['PlayerName', 'playerid', 'POS', 'mRBI', 'mR', 'mSB', 'mHR', 'mOBP', 'PTS', 'aPOS',
                'Dollars']
        }
        self.historical_cols = {
            0: ['PlayerName', 'playerid', 'Throws', 'Age', 'G', 'GS', 'IP', 'SV', 'HLD', 'H', 'BB',
                'HR', 'ER', 'SO', 'BABIP', 'FIP', 'Barrel%', 'HardHit%', 'LD%', 'GB%', 'FB%', 'HR/FB',
                'O-Swing%', 'Z-Swing%', 'O-Contact%', 'Z-Contact%', 'Contact%', 'Zone%', 'SwStr%',
                'CStr%', 'C+SwStr%', 'Pull%', 'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%'],
            1: ['PlayerName', 'playerid', 'Bats', 'Age', 'G', 'PA', 'H', 'BB', 'HR', 'R', 'RBI', 'SB', 'SO', 'CS',
                'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'LD%', 'GB%', 'FB%', 'HR/FB', 'Balls', 'Strikes', 'BB%', 'K%',
                'O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Z-Contact%', 'Contact%', 'SwStr%', 'C+SwStr%', 'Pull%',
                'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%', 'Barrel%', 'maxEV']
        }

    def get_auction_data(self, changes: list) -> dict:
        url = self.auction_url_base
        for change_pair in changes:
            url = url.replace(change_pair[0], change_pair[1])
        response = requests.get(url)
        fg_json = response.json()
        index = 'type=bat' in url
        fg_df: pl.DataFrame = pl.DataFrame(fg_json['data'])
        fg_df = fg_df.select(self.auction_cols[index]['cols_to_keep']).rename(
            self.auction_cols[index]['cols_to_rename'])
        return fg_df
