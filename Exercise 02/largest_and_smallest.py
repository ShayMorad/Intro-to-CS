


def largest_and_smallest(num1, num2, num3):
    """Returns the maximum number and minimum number between the 3 numbers given to the function.
    Returns max first and min second.
    """

    # Setting blank variables for minimum and maximum values.
    min_num = None
    max_num = None

    # Checking for max value.
    if num1 >= num2 and num1 >= num3:
        max_num = num1
    elif num2 >= num1 and num2 >= num3:
        max_num = num2
    else:
        max_num = num3

    # Checking for min value.
    if num1 <= num2 and num1 <= num3:
        min_num = num1
    elif num2 <= num1 and num2 <= num3:
        min_num = num2
    else:
        min_num = num3

    # Returning max and min value.
    return max_num, min_num


def check_largest_and_smallest():
    """This function calls the largest_and_smallest function with chosen parameteres and checks whether
    it returns the expected values. If all expected values were returned, this function will return True.
    False otherwise."""

    # We set a count in order to check if all 5 calls were right or not.
    true_count = 0

    # Checking the first function 5 times with given parameters.
    check1 = largest_and_smallest(17, 1, 6)
    check2 = largest_and_smallest(1, 17, 6)
    check3 = largest_and_smallest(1, 1, 2)
    check4 = largest_and_smallest(0, 0, 0)
    check5 = largest_and_smallest(-50.7, 60.5*2, -132.15)

    # Adding to a count wheter the function worked properly or not so we can evaluate it at the end.
    if check1 == (17, 1):
        true_count += 1

    if check2 == (17, 1):
        true_count += 1

    if check3 == (2, 1):
        true_count += 1

    if check4 == (0, 0):
        true_count += 1

    if check5 == (121, -132.15):
        true_count += 1

    # Returns True if all checks passed and False otherwise.
    return true_count == 5



