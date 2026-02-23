_FALSY = {"false", "0", "no", "off"}
_TRUTHY = {"true", "1", "yes", "on"}


def str_to_bool(value: str) -> bool:
    """Convert common string representations of booleans to actual boolean values."""
    value_lower = value.lower()
    if value_lower in _TRUTHY:
        return True
    elif value_lower in _FALSY:
        return False
    else:
        raise ValueError(f"Cannot convert {value} to boolean.")
