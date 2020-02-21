from pkg_resources import resource_stream
import pandas as pd

print(__name__)
stream = resource_stream(__name__, "data/df_players.pkl")
df_players = pd.read_pickle(stream, compression=None)
df_players = df_players.dropna(subset=["goal_difference"])

stream = resource_stream(__name__, "data/df_matches.pkl")
df_matches = pd.read_pickle(stream, compression=None)
