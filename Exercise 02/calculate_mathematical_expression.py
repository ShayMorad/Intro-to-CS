

def calculate_mathematical_expression(num1, num2, math_expression):
    """This function takes in a mathematical expression and applies it the 2 numbers given to the function.
        If the math expression is ("-"): the function will substract the first number from the second number.
        If the math expression (":"): the function will devide the first number by the second number"""

    # If illegal action function will return None
    if (num2 == 0 and math_expression == ":") or (math_expression not in ["-", "+", "*", ":"]):
        return None

    # Else calculate the expression and return it
    elif math_expression == "-":
        return (num1 - num2)
    elif math_expression == ":":
        return num1 / num2
    elif math_expression == "+":
        return num1 + num2
    elif math_expression == "*":
        return (num1 * num2)


def calculate_from_string(math_expression):
    """This function calculates a simple mathematical equation given to it that includes 2 numbers and one of the following expressions:
    "-","+",":","*" """
    listed_string = math_expression.split(" ")
    return calculate_mathematical_expression(float(listed_string[0]), float(listed_string[2]), listed_string[1])
