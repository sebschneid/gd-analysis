# gd_analysis module imports
from typing import Dict

import streamlit as st

from gd_analysis import df_players, df_matches
from gd_analysis import data, helpers, visualization

player_url_to_name = helpers.get_map_from_url_to_name(df_players, "player")
team_url_to_name = helpers.get_map_from_url_to_name(df_players, "team")

st.title("Goal Difference Project")
st.write("Explore datasets from big 5 leagues.")

st.header("gd90 calculation")
st.markdown(
    """
    (Sum of the goal differences (GD) during each of the appearances) / (total playing time) x 90
"""
)
# st.write("As formula:")
# st.latex(
#     r"""
#     \text{gd90} = \frac{\sum{\text{GD}}}{\sum{\text{min'}} \cdot 90}
# """
# )

# The `gd90` value in plots below is calculated for each player as 90 * SUM(goal difference while player is on field) / SUM(minutes played)
st.header("Analysis for selected season, player and team")

VISIBLE_COLUMNS = [
    "competition",
    "year",
    "matchday",
    "team_name",
    "player_name",
    "goal_difference",
    "duration",
]

competitions = sorted(df_players["competition"].unique())
competition = st.sidebar.selectbox("Select Competition", competitions)
df_competition = data.filter_competition(df_players, competition)

seasons = sorted(df_competition["year"].unique())
season = st.sidebar.selectbox("Select Season", seasons)
df_season = data.filter_season(df_competition, season)

teams = sorted(df_season.sort_values("team_name")["team_url"].unique())
team = st.sidebar.selectbox(
    "Select Team", teams, format_func=team_url_to_name.get,
)
df_team = data.filter_team_url(df_season, team)

min_appearances = st.sidebar.number_input(
    "Filter players with less than input appearances",
    min_value=0,
    max_value=34,
    value=5,
    step=1,
)

fig_season = visualization.scatter_players_for_season(
    df_players,
    df_matches,
    competition,
    season,
    x_column="gd90",
    y_column="full_games",
    min_appearances=min_appearances,
    team=team,
)
st.plotly_chart(fig_season)


fig_team = visualization.scatter_players_for_team(
    df_players=df_players,
    df_matches=df_matches,
    team=team,
    competition=competition,
    season=season,
    x_column="gd90",
    y_column="full_games",
    min_appearances=min_appearances,
)
st.plotly_chart(fig_team)

fig_team_bar = visualization.bar_players_for_team(
    df_players=df_players,
    df_matches=df_matches,
    team=team,
    competition=competition,
    season=season,
    weight_column="full_games",
    min_appearances=min_appearances,
)
st.plotly_chart(fig_team_bar)


players = df_team.sort_values("player_name")["player_url"].unique()
player = st.selectbox(
    "Select Player", players, format_func=player_url_to_name.get
)
df_player = data.filter_player_url(df_team, player)

default_columns = [
    "matchday",
    "goal_difference",
    "duration",
]

selected_columns = st.multiselect(
    "Columns to display", options=VISIBLE_COLUMNS, default=default_columns
)
st.write(df_player[selected_columns].reset_index(drop=True))
