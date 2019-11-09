def get_dash_dropdown_options(values, labels):
    return [
        {"label": label, "value": value} for value, label in zip(values, labels)
    ]
