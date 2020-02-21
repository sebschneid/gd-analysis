from typing import Dict, List


import pandas as pd


def get_dash_dropdown_options(values: List[str], labels: List[str]) -> List[Dict[str, str]]:
    return [
        {"label": label, "value": value} for value, label in zip(values, labels)
    ]


def get_map_from_url_to_name(df: pd.DataFrame, column: str) -> Dict[str, str]:
    df_unique = (
        df[[f"{column}_url", f"{column}_name"]]
        .drop_duplicates()
    )
    url_to_name = dict(
        zip(df_unique[f"{column}_url"], df_unique[f"{column}_name"])
    )
    return url_to_name
