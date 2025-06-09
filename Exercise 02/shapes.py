

import math


def shape_area():
    """This function asks the user to pick from 3 shapes and input the necessary parameters
        in order to calculate their area.
    These are the possible picks:
    1 = Circle
    2 = Rectangle
    3 = Triangle
    Anything else = returns 'None'."""

    # ask user to pick a shape
    user_shape = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")

    if user_shape not in ["1", "2", "3"]:
        return None

    # asks user for input for radius and returns area result
    elif user_shape == "1":
        user_radius = input("")
        return (float(user_radius) ** 2) * math.pi

    # asks user for input for rectangle sides and returns area result
    elif user_shape == "2":
        user_rec_side1 = input("")
        user_rec_side2 = input("")
        return float(user_rec_side1) * float(user_rec_side2)

    # asks user for input for triangle sides and returns area result
    else:
        user_triangle_side = input("")
        return ((3 ** 0.5) * (float(user_triangle_side) ** 2)) / 4
