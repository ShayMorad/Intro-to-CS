

def is_vormir_safe(threshold, day1, day2, day3):
    """
    This function returns True or False whether there were 2 days where the temperature was higher than
    the threshold temperature.
    param threshold: Temperature to pass in order to add to the count of passing the threshold temperature.
    param day1: Temperature of day 1.
    param day2: Temperature of day 2.
    param day3: Temperature of day 3.
    return -  True if in 2 or more days the temperature was higher than the threshold temperature.
                Else returns False.
    """

    # This counts how many days have passed the threshold.
    count = 0
    # Check for day 1.
    if day1 > threshold:
        count += 1
    # Check for day 2.
    if day2 > threshold:
        count += 1
    # Check for day 3.
    if day3 > threshold:
        count += 1
    # If 2 or more days have passed the threshold, returns True. Else, returns False.
    if count >= 2:
        return True
    else:
        return False
