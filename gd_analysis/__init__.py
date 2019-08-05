from pkg_resources import resource_stream
import pandas as pd

stream = resource_stream(__name__, 'data/df_datasets.pkl')
df_datasets = pd.read_pickle(stream, compression=None)
df_datasets = df_datasets.dropna(subset=['goal_difference'])
