import polars as pl
import requests


def get_fangraphs_data(fg_url: str) -> dict:
    response = requests.get(fg_url)
    return response.json()


def return_fg_df(request_type: dict) -> pl.DataFrame:
    fg_json: dict = get_fangraphs_data(request_type['url'])
    fg_df: pl.DataFrame = pl.DataFrame(fg_json['data'])
    fg_df = fg_df.select(request_type['cols_to_keep']).rename(request_type['cols_to_rename'])
    return fg_df

