"""Library of small functions."""


def add_1(x):
    """Add 1 to x."""
    return x + 1


def add_2(x):
    """Add 2 to x."""
    return x + 2


def add_3(x):
    """Add 3 to x."""
    return x + 3


def add_4(x):
    """Add 4 to x."""
    return x + 4


def add_5(x):
    """Add 5 to x."""
    return x + 5


def add_6(x):
    """Add 6 to x."""
    return x + 6


def add_7(x):
    """Add 7 to x."""
    return x + 7


def add_8(x):
    """Add 8 to x."""
    return x + 8


def add_9(x):
    """Add 9 to x."""
    return x + 9


def add_10(x):
    """Add 10 to x."""
    return x + 10


def add_11(x):
    """Add 11 to x."""
    return x + 11


def add_12(x):
    """Add 12 to x."""
    return x + 12


def add_13(x):
    """Add 13 to x."""
    return x + 13


def add_14(x):
    """Add 14 to x."""
    return x + 14


def add_15(x):
    """Add 15 to x."""
    return x + 15


def add_16(x):
    """Add 16 to x."""
    return x + 16


def add_17(x):
    """Add 17 to x."""
    return x + 17


def add_18(x):
    """Add 18 to x."""
    return x + 18


def add_19(x):
    """Add 19 to x."""
    return x + 19


def add_20(x):
    """Add 20 to x."""
    return x + 20


def add_21(x):
    """Add 21 to x."""
    return x + 21


def add_22(x):
    """Add 22 to x."""
    return x + 22


def add_23(x):
    """Add 23 to x."""
    return x + 23


def add_24(x):
    """Add 24 to x."""
    return x + 24


def add_25(x):
    """Add 25 to x."""
    return x + 25


def add_26(x):
    """Add 26 to x."""
    return x + 26


def add_27(x):
    """Add 27 to x."""
    return x + 27


def add_28(x):
    """Add 28 to x."""
    return x + 28


def add_29(x):
    """Add 29 to x."""
    return x + 29


def add_30(x):
    """Add 30 to x."""
    return x + 30


def add_31(x):
    """Add 31 to x."""
    return x + 31


def add_32(x):
    """Add 32 to x."""
    return x + 32


def add_33(x):
    """Add 33 to x."""
    return x + 33


def add_34(x):
    """Add 34 to x."""
    return x + 34


def add_35(x):
    """Add 35 to x."""
    return x + 35


def add_36(x):
    """Add 36 to x."""
    return x + 36


def add_37(x):
    """Add 37 to x."""
    return x + 37


def add_38(x):
    """Add 38 to x."""
    return x + 38


def add_39(x):
    """Add 39 to x."""
    return x + 39


def add_40(x):
    """Add 40 to x."""
    return x + 40


def add_41(x):
    """Add 41 to x."""
    return x + 41


def add_42(x):
    """Add 42 to x."""
    return x + 42


def add_43(x):
    """Add 43 to x."""
    return x + 43


def add_44(x):
    """Add 44 to x."""
    return x + 44


def add_45(x):
    """Add 45 to x."""
    return x + 45


def add_46(x):
    """Add 46 to x."""
    return x + 46


def add_47(x):
    """Add 47 to x."""
    return x + 47


def add_48(x):
    """Add 48 to x."""
    return x + 48


def add_49(x):
    """Add 49 to x."""
    return x + 49


def add_50(x):
    """Add 50 to x."""
    return x + 50


def add_51(x):
    """Add 51 to x."""
    return x + 51


def add_52(x):
    """Add 52 to x."""
    return x + 52


def add_53(x):
    """Add 53 to x."""
    return x + 53


def add_54(x):
    """Add 54 to x."""
    return x + 54


def add_55(x):
    """Add 55 to x."""
    return x + 55


def add_56(x):
    """Add 56 to x."""
    return x + 56


def add_57(x):
    """Add 57 to x."""
    return x + 57


def add_58(x):
    """Add 58 to x."""
    return x + 58


def add_59(x):
    """Add 59 to x."""
    return x + 59


def add_60(x):
    """Add 60 to x."""
    return x + 60


def percentile(values, p):
    """Value at rank p (0-100) using the nearest-rank method."""
    ordered = sorted(values)
    rank = round(p / 100 * len(ordered))
    return ordered[rank - 1]
