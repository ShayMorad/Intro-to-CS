

def input_list():
    """This function asks the user for number inputs. Each input will be appended to a list and the user can end the
    input by typing "". After the user finishes the input, an additional value will be added to the list that is the sum
    of all the numbers the user have input.
    """

    nums_list = []
    counter = 0
    # Loop that keeps running and asking user for input until he types "".
    while True:
        user_input = input()

        counter += 1

        if user_input == "" and counter == 0:
            nums_list.append(0)

        # break the loop if user typed "".
        elif user_input == "":
            break

        # else append the number to a list.
        else:
            user_input = float(user_input)
        nums_list.append(user_input)

    sum_of_inputs = 0
    # This loop sums all the numbers in the list and adds the sum to the end of the list.
    for num in nums_list:
        sum_of_inputs += num
    nums_list.append(sum_of_inputs)

    return nums_list


def inner_product(vec_1, vec_2):
    """This function returns the inner standard multiplication of the vec_1 list and vec_2 list.
    """

    # Return none when the lengths of the lists are different.
    if len(vec_1) != len(vec_2):
        return None

    # Return a [0] list if both vec lists are empty.
    elif vec_1 == [] and vec_2 == []:
        return 0

    # If none of the above conditions were met, calculate the inner standard multiplication of the vec lists.
    elif len(vec_1) == len(vec_2):
        indexes = len(vec_1)
        inner_multi_vec = 0
        for i in range(indexes):
            curr_vec = vec_1[i] * vec_2[i]
            inner_multi_vec += curr_vec
        return inner_multi_vec


def sequence_monotonicity(sequence):
    """This function takes in a list containing numbers and checks for the following conditions:
    1. If each number is <= than the next number after it.
    2. If each number is < than the next number after it.
    3. If each number is >= than the next number after it.
    4. If each number is > than the next number after it.
    After checking all conditions, the function will return a list containing 4 boolean values (True/False) by order,
    that represents whether each condition was met or not.
    For example: if we give the function the following list; [1,2,5,5],
    the function will return the list; [True, False, False, False.
    """

    if sequence == [] or (len(sequence) == 1):
        return [True, True, True, True]

    conditions_met = [False, False, False, False]
    length = len(sequence)

    # Checks for cons 1 and 2.
    for index in range(length - 1):
        if sequence[index] < sequence[index + 1]:
            if index == length - 2:
                conditions_met[0] = True
                conditions_met[1] = True
        else:
            break

    # If con 1 wasn't met by the prior loop, check it again by itself.
    if conditions_met[0] == False:
        for index in range(length - 1):
            if sequence[index] <= sequence[index + 1]:
                if index == length - 2:
                    conditions_met[0] = True
            else:
                break

    # Checks for cons 3 and 4.
    for index in range(length - 1):
        if sequence[index] > sequence[index + 1]:
            if index == length - 2:
                conditions_met[2] = True
                conditions_met[3] = True
        else:
            break

    # If con 3 wasn't met by the prior loop, check it again by itself.
    if conditions_met[2] == False:
        for index in range(length - 1):
            if sequence[index] >= sequence[index + 1]:
                if index == length - 2:
                    conditions_met[2] = True
            else:
                break

    return conditions_met


def monotonicity_inverse(def_bool):
    """ This function takes in a list of 4 boolean values that are True/False, it then creates an example list that
    fulfills the conditions marked 'True' in the list based on the conditions of the sequence_monotonicity function
    by order. If the conditions are impossible to be met, this function will return None.
    """

    if def_bool == [True, False, False, False]:
        return [1, 2, 2, 2]
    elif def_bool == [True, True, False, False]:
        return [1, 2, 3, 4]
    elif def_bool == [False, False, True, False]:
        return [4, 3, 3, 2]
    elif def_bool == [False, False, True, True]:
        return [4, 3, 2, 1]
    elif def_bool == [True, False, True, False]:
        return [1, 1, 1, 1]
    elif def_bool == [False, False, False, False]:
        return [1, 5, 1, -5]
    else:
        return None


def convolve(mat):
    """This function receives a matrix.
    It then returns a matrix where each value starting from the top left (0, 0).
    Each value in it is calculated by summarizing up all numbers in a 3x3 square from the original input matrix,
    then going right within the columns of the original matrix to calculate the second value for the returned matrix,
    and so on.
    After the square right edge reaches the right-most column of the original matrix, it goes back to the starting point
    but lowers 1 row, downwards.
    This goes on until the function calculates the whole returned matrix and returns it.
    """

    # Check for error in input matrix. If error return None.
    if len(mat) == 0 or mat == []:
        return None

    rows = len(mat) - 2
    columns = len(mat[0]) - 2
    list_of_lists = []

    # Create an empty list in the required size as the returned matrix
    for i in range(rows):
        list_of_lists.append([])

    # Calculate the values for each number and append it to the returned matrix
    for x in range(rows):
        for y in range(columns):
            curr_sum = mat[x][y] + mat[x][y + 1] + mat[x][y + 2] + \
                       mat[x + 1][y] + mat[x + 1][y + 1] + mat[x + 1][y + 2] + \
                       mat[x + 2][y] + mat[x + 2][y + 1] + mat[x + 2][y + 2]
            list_of_lists[x].append(curr_sum)
    return list_of_lists


def sum_of_vectors(vec_lst):
    """This function takes in a list of vectors and returns a vector that is the summarization
    of all the different vectors in the list. The input vectors must be of the same length.
    If the input list is empty the function will return 'None'.
    If the vectors in the input list are empty the function will return an empty list = '[]'.
    """

    # Return None and [] in case of conditions mentioned in the function's docstring.
    if len(vec_lst) == 0:
        return None
    elif len(vec_lst[0]) == 0:
        return []

    # Sum vec to return, calculate how many nums in each vector and how many vectors in total.
    summarized_vec = []
    vectors_in_list = len(vec_lst)
    nums_in_vectors = len(vec_lst[0])
    counter = 0

    # While we didn't run the loop as many times as how many numbers in each vector, we continue
    # to calculate and sum each number at the same position in all the vectors then append it
    # to the summarized vector of them all.
    while counter < nums_in_vectors:
        curr_sum = 0
        for i in range(vectors_in_list):
            curr_sum += vec_lst[i][counter]
        counter += 1
        summarized_vec.append(curr_sum)

    return summarized_vec


def num_of_orthogonal(vectors):
    """This function receives a list of vectors.
    The function returns how many vectors are orthogonal out of all the input vectors.
    In order to check, this function calls a previous function names 'inner_product()'.
    """

    if [] in vectors:
        return 0

    # Checks how many separate vectors were given to the function and set a counter to return at the end.
    num_of_vectors = len(vectors)
    orthogonal_vectors = 0

    # We run a loop on each vector, for each vector starting from the [i] vector (ex; i=0 which is the first vector)
    # we check all the following vectors after it to see if they're orthogonal to it.
    for vec in range(num_of_vectors):
        for vec2 in range(vec + 1, num_of_vectors):
            multiplication = inner_product(vectors[vec], vectors[vec2])
            if multiplication == 0:
                orthogonal_vectors += 1
    return orthogonal_vectors
