def page(items, number, size):
    """Return page `number` (the first page is 1)."""
    start = number * size
    return items[start:start + size]


def page_count(items, size):
    return len(items) // size
