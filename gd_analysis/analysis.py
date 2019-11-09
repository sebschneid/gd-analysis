import plotly.graph_objects as go
from .data import get_competition_df, get_season_df, get_team_df, get_player_df


def get_players_goal_differences(df):
    df_grouped = df.groupby(["team", "url", "name"])[
        "duration", "goal_difference"
    ].sum()
    df_grouped["appearances"] = df.groupby(["team", "url", "name"])[
        "duration"
    ].count()
    df_grouped["gd_total"] = (
        df_grouped["goal_difference"] / df_grouped["duration"]
    )
    df_grouped["gd90"] = df_grouped["gd_total"] * 90
    df_grouped["full_games"] = df_grouped["duration"] / 90
    return df_grouped


def get_player_performance_for_matchdays(df, player_url):
    df_player = df[df["url"] == player_url].sort_values(["year", "matchday"])
    goal_differences = df_player["goal_difference"].values
    matchdays = sorted(
        [
            f"{year[:4]}\n{matchday:02}"
            for year, matchday in df_player[["year", "matchday"]].values
        ]
    )
    return matchdays, goal_differences
