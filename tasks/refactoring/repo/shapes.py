import math


def circle_area(radius):
    if radius < 0:
        raise ValueError("negative dimension")
    return math.pi * radius ** 2


def square_area(side):
    if side < 0:
        raise ValueError("negative dimension")
    return side ** 2


def rectangle_area(width, height):
    if width < 0 or height < 0:
        raise ValueError("negative dimension")
    return width * height
