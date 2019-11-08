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
from gd_analysis import df_datasets

from gd_analysis.data import (
    get_competition_df, get_season_df, get_team_df, get_player_df
)
from gd_analysis.visualization import (
    plot_season_overview,
    plot_team_overview
)
from gd_analysis.helpers import get_dash_dropdown_options

PAGE_SIZE = 10
VISIBLE_COLUMNS = ['competition', 'year', 'matchday', 'team', 'name', 'goal_difference', 'duration']

competitions = df_datasets['competition'].unique()
competition_options = get_dash_dropdown_options(competitions, competitions)
seasons = df_datasets['year'].unique()
season_options = get_dash_dropdown_options(seasons, seasons)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(external_stylesheets=external_stylesheets)
app._assets_url_path = 'APP/assets'

app.layout = html.Div(children=[
    html.Section(className="hero has-background-black", style=dict(margin=0, padding=0), children=[
        html.Div(className="hero-body", children=[
            html.Div(className="container has-text-white", children=[
                html.H1("Goal Difference Project", className='title has-text-white'),
                html.H1("Explore datasets from big 5 leagues.", className='subtitle has-text-white')

            ]),
        ])
    ]),
    html.Section(className="section", children=[
        html.Div(className="container", children=[
            html.Div(
                dash_table.DataTable(
                    id='datatable-raw',
                    columns=[{"name": column, "id": column} for column in VISIBLE_COLUMNS],
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action='native',
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                ),
            ),
            dcc.Dropdown(id='dropdown-competition', options=competition_options, value='Bundesliga'),
            dcc.Dropdown(id='dropdown-season', options=season_options, value='2018-19'),
            dcc.Dropdown(id='dropdown-team'),
            dcc.Dropdown(id='dropdown-player'),
            dcc.Graph(id='graph-season-overview'),
            dcc.Graph(id='graph-team-overview'),
        ]),
    ])
])


@app.callback(
    Output('datatable-raw', 'data'),
    [Input('dropdown-competition', 'value'),
     Input('dropdown-season', 'value'),
     Input('dropdown-team', 'value'),
     Input('dropdown-player', 'value'),
     ]
)
def update_datatable_raw(competition, season, team, player_url):
    df = df_datasets
    if competition:
        df = get_competition_df(df, competition)
    if season:
        df = get_season_df(df, season)
    if team:
        df = get_team_df(df, team)
    if player_url:
        df = get_player_df(df, player_url)
    return df[VISIBLE_COLUMNS].to_dict('records')


@app.callback(
    Output('graph-season-overview', 'figure'),
    [Input('dropdown-competition', 'value'),
     Input('dropdown-season', 'value')])
def update_season_overview(competition, season):
    if competition and season:
        return plot_season_overview(df_datasets, competition, season)
    else:
        return go.Figure([])


@app.callback(
    Output('graph-team-overview', 'figure'),
    [Input('dropdown-team', 'value')],
    [State('dropdown-competition', 'value'),
     State('dropdown-season', 'value')]
)
def update_team_overview(team, competition, season):
    if team and competition and season:
        return plot_team_overview(
            df=df_datasets,
            team=team,
            competition=competition,
            season=season,
        )
    else:
        return go.Figure([])


@app.callback(
    Output('dropdown-team', 'options'),
    [Input('dropdown-season', 'value')],
    [State('dropdown-competition', 'value')]
)
def update_dropdown_team_options(season, competition):
    if season and competition:
        df = get_competition_df(df_datasets, competition)
        df = get_season_df(df, season)
        teams = sorted(df['team'].unique())
        return get_dash_dropdown_options(teams, teams)

    else:
        return []


@app.callback(
    Output('dropdown-player', 'options'),
    [Input('dropdown-team', 'value')],
    [State('dropdown-competition', 'value'),
     State('dropdown-season', 'value')]
)
def update_dropdown_team_options(team, competition, season):
    if season and competition and team:
        print(season, competition, team)
        df = get_competition_df(df_datasets, competition)
        df = get_season_df(df, season)
        df = get_team_df(df, team)
        print(df.head())
        player_urls, player_names = df[['url', 'name']] \
            .drop_duplicates().sort_values('name').values.transpose()
        print(player_urls, player_names)
        return get_dash_dropdown_options(player_urls, player_names)

    else:
        return []


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
