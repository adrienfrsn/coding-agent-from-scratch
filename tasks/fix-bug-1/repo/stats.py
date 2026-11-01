def mean(values):
    if not values:
        return 0
    return sum(values) / len(values)


def median(values):
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 0:
        return (ordered[middle] + ordered[middle + 1]) / 2
    return ordered[middle]
