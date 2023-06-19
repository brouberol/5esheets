def is_field_from_checkbox(field_name: str):
    return (
        field_name.endswith(("-prof", "-prepped"))
        or field_name in ("inspiration", "darkvision")
        or field_name.startswith(("deathfail", "deathsuccess"))
    )
