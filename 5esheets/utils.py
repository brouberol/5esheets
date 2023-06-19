from typing import Optional


def is_field_from_checkbox(field_name: str):
    return (
        field_name.endswith(("-prof", "-prepped"))
        or field_name in ("inspiration", "darkvision")
        or field_name.startswith(("deathfail", "deathsuccess"))
    )


def is_not_empty(data: Optional[str | list | dict]) -> bool:
    return data not in (None, "", [], {})


def strip_empties_from_list(data: dict) -> dict:
    new_data = []
    for v in data:
        if isinstance(v, dict):
            v = strip_empties_from_dict(v)
        elif isinstance(v, list):
            v = strip_empties_from_list(v)
        if is_not_empty(v):
            new_data.append(v)
    return new_data


def strip_empties_from_dict(data):
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = strip_empties_from_dict(v)
        elif isinstance(v, list):
            v = strip_empties_from_list(v)
        if is_not_empty(v):
            new_data[k] = v
    return new_data
