
import math


def golden_ratio():
    """Prints the golden ratio."""
    print((1+math.sqrt(5))/2)


def six_squared():
    """Prints the result of six to the power of two."""
    print(math.pow(6, 2))


def hypotenuse():
    """Prints the length of the hypotenuse of a right triangle, that its other 2 sides
    (base and perpendicular sides) lengths are 5 and 12."""
    print(math.sqrt(math.pow(5, 2)+math.pow(12, 2)))


def pi():
    """Prints the value of the constant pi."""
    print(math.pi)


def e():
    """Prints the value of the constant e."""
    print(math.e)


def squares_area():
    """Prints the areas of all the squares of which their sides lengths are 1 to 10. """
    print(1**2, 2**2, 3**2, 4**2, 5**2, 6**2, 7**2, 8**2, 9**2, 10**2)


if __name__ == "__main__":
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
