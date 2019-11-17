from pathlib import Path
import pandas as pd

#DATAPATH = "../gd_analysis/data"
DATAPATH = "./data"

"""
players data format consists of following columns:
    'player_url': url identifying the player
    'player_name': name of the player
    'side': side for which the player played (home, away)
    'team_url': url identifying the team the player played for
    'team_name': name of the team the player played for
    'start': first minute of appearance
    'end': last minute of appearance
    'duration': duration of appearance
    'goal_difference': goal_difference while the appearance of the player
    'matchday': string identifying the matchday
    'competition': string identifying the competition
    'year': string identifying the year
"""


def file_exists(file: str):
    file_to_exist = Path(file)
    return file_to_exist.is_file()


def get_dataset_path(competition: str, season: str, kind: str, path=DATAPATH) -> str:
    return f"{DATAPATH}/df_{kind}_{competition}_{season}.pkl"


def read_dataset(competition: str, season: str, kind: str, path=DATAPATH) -> pd.DataFrame:
    file = get_dataset_path(competition, season, kind, path)
    dataset = pd.read_pickle(file)
    return dataset


def filter_competition(df: pd.DataFrame, competition: str):
    return df.loc[df["competition"] == competition]


def filter_season(df: pd.DataFrame, season: str):
    return df.loc[df["year"] == season]


def filter_team_url(df: pd.DataFrame, team: str):
    return df.loc[df["team_url"] == team]


def filter_player_url(df: pd.DataFrame, player_url: str):
    return df.loc[df["player_url"] == player_url]
