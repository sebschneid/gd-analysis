import plotly.graph_objects as go
from .data import filter_competition, filter_season, filter_team_url, filter_player_url


def goal_difference_for_team(df_matches, team_url: str) -> float:
    team_home_matches = df_matches[df_matches["team_home_url"] == team_url]
    goal_differences_home = (
        team_home_matches["score_home"] - team_home_matches["score_away"]
    )

    team_away_matches = df_matches[df_matches["team_away_url"] == team_url]
    goal_differences_away = (
        team_away_matches["score_away"] - team_away_matches["score_home"]
    )
    count_matches = len(goal_differences_home) + len(goal_differences_away)
    goal_difference_sum = goal_differences_home.sum() + goal_differences_away.sum()

    print(goal_difference_sum / count_matches)
    return goal_difference_sum / count_matches


def get_players_goal_differences(df_player_appearances):
    df_grouped = df_player_appearances.groupby(["team_url", "player_url", "player_name"])[
        "duration", "goal_difference"
    ].sum()
    df_grouped["appearances"] = df_player_appearances.groupby(["team_url", "player_url", "player_name"])[
        "duration"
    ].count()
    df_grouped["gd_total"] = (
        df_grouped["goal_difference"] / df_grouped["duration"]
    )
    df_grouped["gd90"] = df_grouped["gd_total"] * 90
    df_grouped["full_games"] = df_grouped["duration"] / 90
    return df_grouped


def get_player_performance_for_matchdays(df, player_url: str):
    df_player = df[df["player_url"] == player_url].sort_values(["year", "matchday"])
    goal_differences = df_player["goal_difference"].values
    matchdays = sorted(
        [
            f"{year[:4]}\n{matchday:02}"
            for year, matchday in df_player[["year", "matchday"]].values
        ]
    )
    return matchdays, goal_differences
