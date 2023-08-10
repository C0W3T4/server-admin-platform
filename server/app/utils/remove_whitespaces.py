def remove_whitespaces_add_dashes(string: str) -> str:
    return "-".join(string.split()).lower()
