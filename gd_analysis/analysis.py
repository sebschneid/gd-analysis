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


def get_players_gd(df):
    df['gd_per_minute'] = (df['goal_difference'] / df['duration'])
    df_grouped_sum = df.groupby(['team', 'url', 'name'])['gd_per_minute', 'duration', 'goal_difference'].sum()
    df_grouped_mean = df.groupby(['team', 'url', 'name'])['gd_per_minute', 'duration', 'goal_difference'].mean()
    df_grouped_count = df.groupby(['team', 'url', 'name'])['goal_difference'].count()
    df_grouped = df_grouped_sum.merge(df_grouped_mean, on=['team', 'url', 'name'], suffixes=('_sum', '_mean'))
    df_grouped['count_appearences'] = df.groupby(['team', 'url', 'name'])['duration'].count()
    df_grouped['gd90_mean'] = df_grouped['gd_per_minute_mean'] * 90
    df_grouped['gd90_mean2'] =  df_grouped['goal_difference_mean'] * 90 / df_grouped['duration_mean']
    df_grouped['games_played'] = df_grouped['duration_sum'] / 90
    return df_grouped


def get_player_performance_for_matchdays(df, player_url):
    df_player = df[df['url'] == player_url].sort_values(['year', 'matchday'])
    goal_differences = df_player['goal_difference'].values
    matchdays = sorted([f'{year[:4]}\n{matchday:02}' for year, matchday in df_player[['year', 'matchday']].values])
    return matchdays, goal_differences


def plot_season_overview(df, competition, season):
    df = get_competition_df(df, competition)
    df = get_season_df(df, season)
   
    df_grouped = get_players_gd(df)
    gd_column = 'gd90_mean2'
    games_played = df_grouped['games_played'].values
    gd_values = df_grouped[gd_column].values
    teams = df_grouped.index.get_level_values(0)
    players = df_grouped.index.get_level_values(2)

    trace = go.Scatter(
        x=gd_values,
        y=games_played,
        mode='markers',
        hovertext = [f'{team}<br>{player}<br>{gd_column}={gd:.1f}<br>Games={games:.1f}' 
                     for team, player, gd, games in zip(teams, players, gd_values, games_played)],
        hoverinfo='text'
    )
    
    data = [trace]

    fig = go.Figure(data, layout=go.Layout())
    
    return fig


def plot_team_overview(df, competition, season, team):
    column = 'gd90_mean2'
    df = get_competition_df(df, competition)
    df = get_season_df(df, season)
    df = get_team_df(df, team)
    df = get_players_gd(df)
    # display(df.head())

    #df_team = df_grouped[df_grouped.index.get_level_values(0) == team]

    player_names = df.index.get_level_values(2)

    trace = go.Scatter(
        x=df[column],
        y=df['games_played'],
        mode="markers+text",
        name="Players",
        text=player_names,
        textposition="top center"
    )

    fig = go.Figure([trace], layout=go.Layout())

    return fig
