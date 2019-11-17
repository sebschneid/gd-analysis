import plotly.graph_objects as go

from gd_analysis.analysis import get_players_goal_differences, goal_difference_for_team
from gd_analysis.data import (
    filter_competition,
    filter_season,
    filter_team_url,
    filter_player_url,
)

TITLE_FONT = {"size": 40, "color": "white"}
LABEL_FONT = {"size": 28, "color": "white"}
TICK_FONT = {"size": 18, "color": "white"}
LEGEND_FONT = {"size": 20, "color": "white"}
PLAYER_TEXT_FONT = {"size": 18, "color": "white"}
ANNOTATION_TEXT_FONT = {"size": 18, "color": "white"}

PLOT_BACKGROUND_COLOR = "rgba(35, 35, 35, 1)"


EMPTY_LAYOUT = go.Layout(
    height=500,
    paper_bgcolor=PLOT_BACKGROUND_COLOR,
    plot_bgcolor=PLOT_BACKGROUND_COLOR,
    xaxis={"showgrid": False},
    yaxis={"showgrid": False},
)


def get_default_layout(title, x_axis_title, y_axis_title, height=500):
    layout = go.Layout(
        height=height,
        title={"text": f"<b>{title}</b>", "font": TITLE_FONT},
        paper_bgcolor=PLOT_BACKGROUND_COLOR,
        plot_bgcolor=PLOT_BACKGROUND_COLOR,
        xaxis={
            "title": f"{x_axis_title}",
            "showgrid": True,
            "zeroline": True,
            "ticks": "outside",
            "tickwidth": 1.5,
            "tickfont": TICK_FONT,
            "tickcolor": "white",
            "gridwidth": 0.5,
            "gridcolor": "grey",
            "title_font": LABEL_FONT,
        },
        yaxis={
            "title": f"{y_axis_title}",
            "showgrid": False,
            "zeroline": True,
            "ticks": "outside",
            "tickwidth": 1.5,
            "tickfont": TICK_FONT,
            "tickcolor": "white",
            "title_font": LABEL_FONT,
            "showline": True,
            "linewidth": 2,
            "linecolor": "white",
            "gridwidth": 0.5,
            "gridcolor": "grey",
        },
        legend=go.layout.Legend(
            x=0.1, y=1.07, font=LEGEND_FONT, orientation="h"
        ),
    )
    return layout


def get_scatter_for_df(
    df,
    x_column,
    y_column,
    name,
    marker_color="lightslategrey",
    line_color="white",
    marker_size=10,
    marker_symbol="circle",
):
    x_values = df[x_column].values
    y_values = df[y_column].values
    teams = df.index.get_level_values(0)
    players = df.index.get_level_values(2)

    return go.Scatter(
        x=x_values,
        y=y_values,
        name=name,
        mode="markers",
        marker={
            "color": marker_color,
            "size": marker_size,
            "line": {"width": 0, "color": line_color},
            "symbol": marker_symbol,
        },
        hovertext=[
            f"{team}<br>{player}<br>{x_column}={x:.1f}<br>{y_column}={y:.1f}"
            for team, player, x, y in zip(teams, players, x_values, y_values)
        ],
        hoverinfo="text",
    )


def scatter_players_for_season(
    df_players,
    df_matches,
    competition: str,
    season: str,
    x_column: str,
    y_column: str,
    min_appearances: int = 5,
    team: "str" = None,
):
    df_players = filter_competition(df_players, competition)
    df_players = filter_season(df_players, season)

    df_grouped = get_players_goal_differences(df_players)
    df_grouped = df_grouped[df_grouped["appearances"] > min_appearances]

    teams = df_grouped.index.get_level_values(0)
    players = df_grouped.index.get_level_values(2)

    data = []

    if team is not None:
        trace_team = get_scatter_for_df(
            df_grouped.loc[[team]],
            x_column,
            y_column,
            name=team,
            marker_color="mediumvioletred",
            marker_symbol="diamond",
        )
        data.append(trace_team)
        df_grouped = df_grouped.drop(index=team)

    trace_all = get_scatter_for_df(
        df_grouped, x_column, y_column, name="All / other teams"
    )
    data.append(trace_all)

    layout = get_default_layout("Season Player Overview", x_column, y_column)
    layout.yaxis.update(rangemode="tozero")

    if team is not None:
        # get mean value for team
        df_matches = filter_competition(df_matches, competition)
        df_matches = filter_season(df_matches, season)
        team_goal_difference = goal_difference_for_team(df_matches, team)

        # for goal difference of team
        shapes = [
            go.layout.Shape(
                type="line",
                yref='paper',
                x0=team_goal_difference,
                y0=0,
                x1=team_goal_difference,
                y1=1,
                line=dict(
                    color="mediumvioletred",
                    width=4,
                    dash="dash",
                ),
            )]
        layout.update(shapes=shapes)

    #  fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10)
    #  fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, col=1)

    fig = go.Figure(data, layout=layout)

    return fig


def scatter_players_for_team(
    df_players,
    df_matches,
    competition,
    season,
    team,
    x_column="gd90",
    y_column="appearances",
    min_appearances: int = 5,
):
    column = "gd90"
    df_players = filter_competition(df_players, competition)
    df_players = filter_season(df_players, season)
    df_players = filter_team_url(df_players, team)
    df_players = get_players_goal_differences(df_players)
    df_players = df_players[df_players["appearances"] > min_appearances]

    # display(df.head())

    # get mean value for team
    df_matches = filter_competition(df_matches, competition)
    df_matches = filter_season(df_matches, season)
    team_goal_difference = goal_difference_for_team(df_matches, team)


    # df_team = df_grouped[df_grouped.index.get_level_values(0) == team]

    player_names = df_players.index.get_level_values(2)

    trace = go.Scatter(
        x=df_players[x_column],
        y=df_players[y_column],
        mode="markers+text",
        name="Players",
        text=player_names,
        textposition="top center",
        marker={"color": "mediumvioletred", "size": 12, "symbol": "diamond",},
        textfont=PLAYER_TEXT_FONT,
    )

    # get mean value for team
    df_matches = filter_competition(df_matches, competition)
    df_matches = filter_season(df_matches, season)
    team_goal_difference = goal_difference_for_team(df_matches, team)

    # for goal difference of team
    shapes = [
        go.layout.Shape(
            type="line",
            yref='paper',
            x0=team_goal_difference,
            y0=0,
            x1=team_goal_difference,
            y1=1,
            line=dict(
                color="mediumvioletred",
                width=3,
                dash="dash",
            ),
        )]

    layout = get_default_layout("Team Player Overview", x_column, y_column)
    layout.yaxis.update(rangemode="tozero")
    layout.update(shapes=shapes)

    fig = go.Figure([trace], layout=layout)

    return fig


def bar_players_for_team(
    df_players,
    df_matches,
    competition,
    season,
    team,
    column="gd90",
    weight_column="appearances",
    min_appearances: int = 5,
):
    df_players = filter_competition(df_players, competition)
    df_players = filter_season(df_players, season)
    df_players = filter_team_url(df_players, team)

    df_players = get_players_goal_differences(df_players)

    df_players = df_players[df_players["appearances"] > min_appearances]
    df_players = df_players.sort_values(column)

    values = df_players[column]
    players = df_players.index.get_level_values(2)
    width_weights = df_players[weight_column]

    # get mean value for team
    df_matches = filter_competition(df_matches, competition)
    df_matches = filter_season(df_matches, season)
    team_goal_difference = goal_difference_for_team(df_matches, team)

    trace = go.Bar(
        x=players,
        y=df_players[column],
        width=0.05 + 0.7 * ((width_weights / width_weights.max())),
        orientation="v",
        hoverinfo="text",
        hovertext=[
            f"<b>{player}</b><br>{column}={value:.1f}<br>{weight_column}={weight:.1f}"
            for player, value, weight in zip(players, values, width_weights)
        ],
        marker={"color": "mediumvioletred", "line": {"width": 0}},
    )

    layout = get_default_layout("Team Player Overview", "Player", column)
    annotations = [
        go.layout.Annotation(
            x=1.0,
            y=1.15,
            xref="paper",
            xanchor="right",
            yanchor="middle",
            yref="paper",
            text="Bar width corresponds to number of occurances.",
            font=ANNOTATION_TEXT_FONT,
        )
    ]

    shapes = [go.layout.Shape(
        type="line",
        xref='paper',
        x0=0,
        y0=team_goal_difference,
        x1=1,
        y1=team_goal_difference,
        line=dict(
            color="mediumvioletred",
            width=4,
            dash="dash",
        ),
    )]

    layout.update(annotations=annotations, shapes=shapes)
    layout.xaxis.update(showgrid=False)
    layout.yaxis.update(showgrid=True)


    data = [trace]

    fig = go.Figure(data=data, layout=layout)

    return fig
