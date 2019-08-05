from pathlib import Path
import pandas as pd

DATAPATH = '../data'


def file_exists(file):
    file_to_exist = Path(file)
    return file_to_exist.is_file()


def get_dataset_path(competition, season):
    return f'{DATAPATH}/df_players_{competition}_{season}.pkl'


def read_dataset(competition, season):
    file = get_dataset_path(competition, season)
    dataset = pd.read_pickle(file)
    return dataset


def get_competition_df(df, competition):
    return df.loc[df['competition'] == competition]


def get_season_df(df, season):
    return df.loc[df['year'] == season]


def get_team_df(df, team):
    return df.loc[df['team'] == team]


def get_player_df(df, player_url):
    return df.loc[df['url'] == player_url]