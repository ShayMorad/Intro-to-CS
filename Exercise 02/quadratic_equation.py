

def quadratic_equation(a, b, c):
    """This function returns the solutions to a quadratic equation.
    In case of less than 2 solutions, the function will return None values for no solution."""

    # calculation of the root in the quadratic formula
    square_root_base = (b ** 2 - 4 * a * c)

    # if the root is negative it means there are no solutions
    if square_root_base < 0:
        return None, None

    # if the root equals 0 it means there's a single solution
    elif square_root_base == 0:
        return (-b) / (2 * a), None

    # if the root is positive there are 2 solutions
    first_solution = ((-b) + square_root_base ** 0.5) / 2 * a
    second_solution = ((-b) - square_root_base ** 0.5) / 2 * a
    return first_solution, second_solution

def quadratic_equation_user_input():
    """This function asks the user for 3 inputs; a, b ,c.
    The user must input the values correctly as numbers (int or float) with 1 space between each number.
    Example: "1 -8 16" """

    # asking user for input
    user_input = input("Insert coefficients a, b, and c: ").split(" ")
    a = float(user_input[0])
    b = float(user_input[1])
    c = float(user_input[2])
    solutions = quadratic_equation(a, b, c)

    # if the user inputs a=0 we tell him it may not be 0.
    if a == 0:
        print("The parameter 'a' may not equal 0")
        return None

    # giving results in case there are 2 solutions.
    elif None not in solutions:
        x, y = solutions
        print(f"The equation has 2 solutions: {x} and {y}")

    # giving result in case where there are no solutions.
    elif solutions == (None, None):
        print("The equation has no solutions")

    # giving result in case where there is 1 solution.
    else:
        x, y = solutions
        if x is not None:
            print(f"The equation has 1 solution: {x}")
        else:
            print(f"The equation has 1 solution: {y}")
