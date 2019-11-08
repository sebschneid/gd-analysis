import plotly.graph_objects as go

from gd_analysis.analysis import get_players_goal_differences
from gd_analysis.data import get_competition_df, get_season_df, get_team_df, get_player_df


def plot_season_overview(df, competition, season):
    df = get_competition_df(df, competition)
    df = get_season_df(df, season)

    df_grouped = get_players_goal_differences(df)
    gd_column = 'gd90'
    full_games = df_grouped['full_games'].values
    gd_values = df_grouped[gd_column].values
    teams = df_grouped.index.get_level_values(0)
    players = df_grouped.index.get_level_values(2)

    trace = go.Scatter(
        x=gd_values,
        y=full_games,
        mode='markers',
        hovertext=[
            f'{team}<br>{player}<br>{gd_column}={gd:.1f}<br>Games={games:.1f}'
             for team, player, gd, games in
             zip(teams, players, gd_values, full_games)
            ],
        hoverinfo='text'
    )

    data = [trace]

    fig = go.Figure(data, layout=go.Layout())

    return fig


def plot_team_overview(df, competition, season, team):
    column = 'gd90'
    df = get_competition_df(df, competition)
    df = get_season_df(df, season)
    df = get_team_df(df, team)
    df = get_players_goal_differences(df)
    # display(df.head())

    #df_team = df_grouped[df_grouped.index.get_level_values(0) == team]

    player_names = df.index.get_level_values(2)

    trace = go.Scatter(
        x=df[column],
        y=df['full_games'],
        mode="markers+text",
        name="Players",
        text=player_names,
        textposition="top center"
    )

    fig = go.Figure([trace], layout=go.Layout())

    return fig
