import plotly.graph_objects as go
from .data import get_competition_df, get_season_df, get_team_df, get_player_df


def get_players_gd_methods(df, player_column='name', team_column='team', method='gd90_per_game'):
    """Summary

    Parameters
    ----------
    df_players : pd.DataFrame
        DataFrame with goal_difference stats.
    player_column : str, optional
        Column for the player's name in the DataFrame
    team_column : str, optional
        Column for the team's name in the DataFrame
    method : str, optional
        Method to evaluate a players goal difference.
        - 'gd90_per_game': Goal difference for each game is summed up, each divided by duration. So SUM[90 * (game_gd / game_duration); all games].
        - 'gd90_overall': Goal difference for each game is summed up, divided by duration in the end. So SUM[90 * game_gd; all games] / SUM[game_duration; all_games]
        - 'gd90_mean': Goal difference for each game is summed and divided by the number of game participations. So SUM[game_gd; all games] / N(games)
        - 'gdsum': Goal difference is summed up for each game.
    """
    
    df['gd90_per_game'] = (df['goal_difference'] / df['duration'])
    
    if method=='gd90_mean':
        df_season = df.groupby([team_column, player_column])['goal_difference', 'duration', 'gd90_per_game'].mean()
        df_season['games_played'] = df.groupby([team_column, player_column])['duration'].sum() / 90
        df_season['gd90_mean'] = df_season['gd90_per_game']
        return df_season[['gd90_mean', 'duration', 'goal_difference', 'games_played']]
    else:  
        df_season = df.groupby([team_column, player_column])['goal_difference', 'duration', 'gd90_per_game'].sum()
        df_season['games_played'] = df_season['duration'] / 90

        if method == 'gd90_per_game':
            return df_season[['gd90_per_game', 'duration', 'goal_difference', 'games_played']]

        if method == 'gd90_overall':
            df_season['gd90_overall'] = df_season['goal_difference'] / df_season['duration']
            return df_season[['gd90_overall', 'duration', 'games_played']]

        if method == 'gdsum':
            df_season['gdsum'] = df_season['goal_difference']
            return df_season[['gdsum', 'duration', 'games_played']]


def get_players_goal_differences(df):
    df_grouped = df.groupby(['team', 'url', 'name'])['duration', 'goal_difference'].sum()
    df_grouped['appearances'] = df.groupby(['team', 'url', 'name'])['duration'].count()
    df_grouped['gd_total'] = df_grouped['goal_difference'] / df_grouped['duration']
    df_grouped['gd90'] = df_grouped['gd_total'] * 90
    df_grouped['full_games'] = df_grouped['duration'] / 90
    return df_grouped


def get_player_performance_for_matchdays(df, player_url):
    df_player = df[df['url'] == player_url].sort_values(['year', 'matchday'])
    goal_differences = df_player['goal_difference'].values
    matchdays = sorted([f'{year[:4]}\n{matchday:02}' for year, matchday in df_player[['year', 'matchday']].values])
    return matchdays, goal_differences

