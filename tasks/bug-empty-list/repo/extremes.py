def maximum(values):
    """Largest value, or None if the list is empty."""
    result = values[0]
    for v in values:
        if v > result:
            result = v
    return result
