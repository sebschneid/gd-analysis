# basic python imports
import pandas as pd

# dash and plotly imports
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

# gd_analysis module imports
from gd_analysis import df_players, df_matches

from gd_analysis.data import (
    filter_competition,
    filter_season,
    filter_team_url,
    filter_player_url,
)
from gd_analysis.visualization import (
    scatter_players_for_season,
    scatter_players_for_team,
    bar_players_for_team,
    EMPTY_LAYOUT,
)
from gd_analysis.helpers import get_dash_dropdown_options

PAGE_SIZE = 10
VISIBLE_COLUMNS = [
    "competition",
    "year",
    "matchday",
    "team_name",
    "player_name",
    "goal_difference",
    "duration",
]

competitions = df_players["competition"].unique()
competition_options = get_dash_dropdown_options(competitions, competitions)
seasons = df_players["year"].unique()
season_options = get_dash_dropdown_options(seasons, seasons)

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.css",
]
app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server

GRAPH_STYLE = {"width": "100%", "marginTop": "50px"}
DROPDOWN_STYLE = {"marginBottom": "20px"}
COLUMN_STYLE = {"marginLeft": "0px", "marginRight": "0px"}

app.layout = html.Div(
    children=[
        html.Section(
            className="hero has-background-black",
            style=dict(margin=0, padding=0),
            children=[
                html.Div(
                    className="hero-body",
                    children=[
                        html.Div(
                            className="container has-text-white",
                            children=[
                                html.H1(
                                    "Goal Difference Project",
                                    className="title has-text-white",
                                ),
                                html.H1(
                                    "Explore datasets from big 5 leagues.",
                                    className="subtitle has-text-white",
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Section(
            className="section",
            children=[
                html.Div(
                    className="container",
                    children=[
                        html.H1(
                            "Raw data table",
                            className="title is-2 has-text-black",
                        ),
                        dcc.Markdown(
                            """
                            **Filter table examples**

                            * To find *Borussia Dortmund* in team column type either `Dort` or `="Borussia Dortmund"`.
                            * To find *Weigl* in player column type `=Weigl`.
                            * To get the second half of the Bundesligaa season type `>17` in matchdays column.
                            * To find players with negative goal differences type `<0` in goal_difference column.

                            ---
                            """,
                            style={"marginBottom": "20px"},
                        ),
                        html.Div(
                            dash_table.DataTable(
                                id="datatable-raw",
                                columns=[
                                    {"name": column, "id": column}
                                    for column in VISIBLE_COLUMNS
                                ],
                                page_current=0,
                                page_size=PAGE_SIZE,
                                page_action="native",
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                style_header={
                                    "backgroundColor": "rgb(30, 30, 30)"
                                },
                                style_cell={
                                    "backgroundColor": "rgb(50, 50, 50)",
                                    "color": "white",
                                },
                                style_filter={
                                    "backgroundColor": "rgb(200, 200, 200)",
                                },
                            ),
                        ),
                        # dropdown elements
                        html.Div(
                            className="container",
                            style={"marginTop": "20px"},
                            children=[
                                html.Div(
                                    className="columns",
                                    children=[
                                        # competition
                                        html.Div(
                                            className="column is-3",
                                            style=COLUMN_STYLE,
                                            children=[
                                                html.Label(
                                                    "Competition",
                                                    className="has-text-weight-bold",
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-competition",
                                                    options=competition_options,
                                                    value="Bundesliga",
                                                ),
                                            ],
                                        ),
                                        # season
                                        html.Div(
                                            className="column is-3",
                                            style=COLUMN_STYLE,
                                            children=[
                                                html.Label(
                                                    "Season",
                                                    className="has-text-weight-bold",
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-season",
                                                    options=season_options,
                                                    value="2018-19",
                                                ),
                                            ],
                                        ),
                                        # team
                                        html.Div(
                                            className="column is-3",
                                            style=COLUMN_STYLE,
                                            children=[
                                                html.Label(
                                                    "Team",
                                                    className="has-text-weight-bold",
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-team"
                                                ),
                                            ],
                                        ),
                                        # player
                                        html.Div(
                                            className="column is-3",
                                            style=COLUMN_STYLE,
                                            children=[
                                                html.Label(
                                                    "Player",
                                                    className="has-text-weight-bold",
                                                ),
                                                dcc.Dropdown(
                                                    id="dropdown-player"
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dcc.Markdown(
                            """
                            ---
                                                       
                            **GD90**
                            
                            The `gd90` value in plots below is calculated for each player as 90 * SUM(goal difference while player is on field) / SUM(minutes played)
                            
                            """,
                            style={"marginBottom": "20px"},
                        ),
                        dcc.Graph(
                            id="graph-season-overview", style=GRAPH_STYLE
                        ),
                        dcc.Graph(id="graph-team-overview", style=GRAPH_STYLE),
                        dcc.Graph(id="graph-team-bars", style=GRAPH_STYLE),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("datatable-raw", "data"),
    [
        Input("dropdown-competition", "value"),
        Input("dropdown-season", "value"),
        Input("dropdown-team", "value"),
        Input("dropdown-player", "value"),
    ],
)
def update_datatable_raw(competition, season, team, player_url):
    df = df_players
    if competition:
        df = filter_competition(df, competition)
    if season:
        df = filter_season(df, season)
    if team:
        df = filter_team_url(df, team)
    if player_url:
        df = filter_player_url(df, player_url)
    return df[VISIBLE_COLUMNS].to_dict("records")


@app.callback(
    Output("graph-season-overview", "figure"),
    [
        Input("dropdown-competition", "value"),
        Input("dropdown-season", "value"),
        Input("dropdown-team", "value"),
    ],
)
def show_season_scatter(competition, season, team):
    if competition and season:
        return scatter_players_for_season(
            df_players,
            df_matches,
            competition,
            season,
            x_column="gd90",
            y_column="appearances",
            team=team,
        )
    else:
        return go.Figure([], layout=EMPTY_LAYOUT)


@app.callback(
    Output("graph-team-overview", "figure"),
    [Input("dropdown-team", "value")],
    [State("dropdown-competition", "value"), State("dropdown-season", "value")],
)
def show_team_scatter(team, competition, season):
    if team and competition and season:
        return scatter_players_for_team(
            df_players=df_players,
            df_matches=df_matches,
            team=team,
            competition=competition,
            season=season,
        )
    else:
        return go.Figure([], layout=EMPTY_LAYOUT)


@app.callback(
    Output("graph-team-bars", "figure"),
    [Input("dropdown-team", "value")],
    [State("dropdown-competition", "value"), State("dropdown-season", "value")],
)
def show_team_bars(team, competition, season):
    if team and competition and season:
        return bar_players_for_team(
            df_players=df_players,
            df_matches=df_matches,
            team=team,
            competition=competition,
            season=season,
        )
    else:
        return go.Figure([], layout=EMPTY_LAYOUT)


@app.callback(
    Output("dropdown-team", "options"),
    [Input("dropdown-season", "value"), Input("dropdown-competition", "value")],
)
def update_dropdown_team_options(season, competition):
    if season and competition:
        df = filter_competition(df_players, competition)
        df = filter_season(df, season)
        teams = sorted(df["team_url"].unique())
        return get_dash_dropdown_options(teams, teams)

    else:
        return []


@app.callback(
    Output("dropdown-player", "options"),
    [Input("dropdown-team", "value")],
    [State("dropdown-competition", "value"), State("dropdown-season", "value")],
)
def update_dropdown_team_options(team, competition, season):
    if season and competition and team:
        df = filter_competition(df_players, competition)
        df = filter_season(df, season)
        df = filter_team_url(df, team)
        player_urls, player_names = (
            df[["player_url", "player_name"]]
            .drop_duplicates()
            .sort_values("player_name")
            .values.transpose()
        )
        return get_dash_dropdown_options(player_urls, player_names)

    else:
        return []


if __name__ == "__main__":
    app.run_server(debug=True)
