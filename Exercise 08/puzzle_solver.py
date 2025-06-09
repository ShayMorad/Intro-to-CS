
import copy
from typing import List, Tuple, Set, Optional

# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function returns how many cells can the current cell see in maximum (-1 cells are treated as 1)"""
    if len(picture) == 0:
        return 0
    if len(picture[0]) == 0:
        return 0
    return _helper_max_seen_cell(picture, row, col, 0)


def _helper_max_seen_cell(picture: Picture, row: int, col: int, sum: int) -> int:
    """
    This function checks for some conditions and when met count the cells in 4 directions from the current cell.
    """
    if row > len(picture) - 1 or row < 0:
        return 0
    if col > len(picture[0]) - 1 or col < 0:
        return 0
    cell = picture[row][col]
    if cell == 0:
        return 0
    sum = 1
    length_row = len(picture)
    length_col = len(picture[0])
    if 0 < row < (len(picture) - 1):
        if picture[row - 1][col] != 0:
            curr = _directions_max_seen_cell(picture, row - 1, col, "up", 0)
            sum += curr
        if picture[row + 1][col] != 0:
            curr = _directions_max_seen_cell(picture, row + 1, col, "down", 0)
            sum += curr

    elif row == (len(picture) - 1) and length_row > 1:
        if picture[row - 1][col] != 0:
            curr = _directions_max_seen_cell(picture, row - 1, col, "up", 0)
            sum += curr

    elif row == 0 and length_row > 1:
        if picture[row + 1][col] != 0:
            curr = _directions_max_seen_cell(picture, row + 1, col, "down", 0)
            sum += curr

    if 0 < col < (len(picture[row]) - 1):
        if picture[row][col - 1] != 0:
            curr = _directions_max_seen_cell(picture, row, col - 1, "left", 0)
            sum += curr
        if picture[row][col + 1] != 0:
            curr = _directions_max_seen_cell(picture, row, col + 1, "right", 0)
            sum += curr

    elif col == 0 and length_col > 1:
        if picture[row][col + 1] != 0:
            curr = _directions_max_seen_cell(picture, row, col + 1, "right", 0)
            sum += curr

    elif col == len(picture[row]) - 1 and length_col > 1:
        if picture[row][col - 1] != 0:
            curr = _directions_max_seen_cell(picture, row, col - 1, "left", 0)
            sum += curr
    return sum


def _directions_max_seen_cell(picture: Picture, row: int, col: int, direction: str, sum: int) -> int:
    """
    This function count the cells in the direction from the current cell that was input.
    """
    if row > len(picture) - 1 or row < 0:
        return sum
    if col > len(picture[0]) - 1 or col < 0:
        return sum
    cell = picture[row][col]
    if cell == 0:
        return sum
    sum += 1
    if direction == "up":
        return _directions_max_seen_cell(picture, row - 1, col, "up", sum)
    elif direction == "down":
        return _directions_max_seen_cell(picture, row + 1, col, "down", sum)
    elif direction == "left":
        return _directions_max_seen_cell(picture, row, col - 1, "left", sum)
    elif direction == "right":
        return _directions_max_seen_cell(picture, row, col + 1, "right", sum)


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """This function returns how many cells can the current cell see in maximum (-1 cells are treated as 0)"""
    if len(picture) == 0:
        return 0
    if len(picture[0]) == 0:
        return 0
    return _helper_min_seen_cell(picture, row, col, 0)


def _helper_min_seen_cell(picture: Picture, row: int, col: int, sum: int) -> int:
    """
    This function checks for some conditions and when met count the cells in 4 directions from the current cell.
    """
    if row > len(picture) - 1 or row < 0:
        return 0
    if col > len(picture[0]) - 1 or col < 0:
        return 0
    cell = picture[row][col]
    if cell == 0 or cell == -1:
        return 0
    sum = 1
    length_row = len(picture)
    length_col = len(picture[0])
    if 0 < row < (len(picture) - 1):
        if picture[row - 1][col] == 1:
            curr = _directions_min_seen_cell(picture, row - 1, col, "up", 0)
            sum += curr
        if picture[row + 1][col] == 1:
            curr = _directions_min_seen_cell(picture, row + 1, col, "down", 0)
            sum += curr

    elif row == (len(picture) - 1) and length_row > 1:
        if picture[row - 1][col] == 1:
            curr = _directions_min_seen_cell(picture, row - 1, col, "up", 0)
            sum += curr

    elif row == 0 and length_row > 1:
        if picture[row + 1][col] == 1:
            curr = _directions_min_seen_cell(picture, row + 1, col, "down", 0)
            sum += curr

    if 0 < col < (len(picture[row]) - 1):
        if picture[row][col - 1] == 1:
            curr = _directions_min_seen_cell(picture, row, col - 1, "left", 0)
            sum += curr
        if picture[row][col + 1] == 1:
            curr = _directions_min_seen_cell(picture, row, col + 1, "right", 0)
            sum += curr

    elif col == 0 and length_col > 1:
        if picture[row][col + 1] == 1:
            curr = _directions_min_seen_cell(picture, row, col + 1, "right", 0)
            sum += curr

    elif col == len(picture[row]) - 1 and length_col > 1:
        if picture[row][col - 1] == 1:
            curr = _directions_min_seen_cell(picture, row, col - 1, "left", 0)
            sum += curr
    return sum


def _directions_min_seen_cell(picture: Picture, row: int, col: int, direction: str, sum: int) -> int:
    """
    This function count the cells in the direction from the current cell that was input.
    """
    if row > len(picture) - 1 or row < 0:
        return sum
    if col > len(picture[0]) - 1 or col < 0:
        return sum
    cell = picture[row][col]
    if cell == 0 or cell == -1:
        return sum
    sum += 1
    if direction == "up":
        return _directions_min_seen_cell(picture, row - 1, col, "up", sum)
    elif direction == "down":
        return _directions_min_seen_cell(picture, row + 1, col, "down", sum)
    elif direction == "left":
        return _directions_min_seen_cell(picture, row, col - 1, "left", sum)
    elif direction == "right":
        return _directions_min_seen_cell(picture, row, col + 1, "right", sum)


def check_constraint_may_exist(picture, row, col, seen):
    """Returns whether a constraint may exist"""
    if min_seen_cells(picture, row, col) == max_seen_cells(picture, row, col) == seen:
        return 1
    elif min_seen_cells(picture, row, col) <= seen <= max_seen_cells(picture, row, col):
        return 2
    return 0


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """Checks for constraints conditions in the picture."""
    total_conditions = []
    for constraint in constraints_set:
        row, col, seen = constraint
        total_seen = check_constraint_may_exist(picture, row, col, seen)
        if total_seen == 1:
            total_conditions.append(1)
        elif total_seen == 2:
            total_conditions.append(2)
        else:
            total_conditions.append(0)
    if 0 in total_conditions:
        return 0
    elif 2 in total_conditions:
        return 2
    return 1


def init_picture(n, m):
    """Creates an empty board with ? cells in it (-1 values)."""
    picture = []
    for row in range(n):
        row = []
        for col in range(m):
            row.append(-1)
        picture.append(row)
    return picture


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """Returns a solution for a board if it exists. If not, returns None."""
    picture = init_picture(n, m)
    return _helper_solve_puzzle(picture, constraints_set, 0, 0)


def _helper_solve_puzzle(picture, constraints, row, col):
    """A helper function for the solve_puzzle function. This function sets recursively values in cells (0 or 1) as long
    as they don't give back a back constraints check (0). When the whole board is filled and the constraints check is
    good, returns the picture."""
    length_row = len(picture) - 1
    length_col = len(picture[0]) - 1
    if check_constraints(picture, constraints) == 0:
        return None
    if (check_constraints(picture, constraints) == 1) and row == length_row and col > length_col:
        return picture
    if row > length_row:
        return None
    if col > length_col:
        return _helper_solve_puzzle(picture, constraints, row + 1, 0)
    picture[row][col] = 0
    recursion = _helper_solve_puzzle(picture, constraints, row, col + 1)
    if recursion is not None:
        return recursion
    picture[row][col] = 1
    recursion = _helper_solve_puzzle(picture, constraints, row, col + 1)
    if recursion is not None:
        return recursion
    picture[row][col] = -1
    return None


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """This function returns the count of how many possible solutions exist."""
    picture = init_picture(n, m)
    return _helper_how_many_solutions(picture, constraints_set, 0, 0, 0)


def _helper_how_many_solutions(picture, constraints, row, col, counter):
    """
    A helper function for the how_many_solutions function, that works recursively.
    """
    length_row = len(picture) - 1
    length_col = len(picture[0]) - 1
    if check_constraints(picture, constraints) == 0:
        return 0
    if (check_constraints(picture, constraints) == 1) and row == length_row and col > length_col:
        return 1
    if row > length_row:
        return 0
    if col > length_col:
        return _helper_how_many_solutions(picture, constraints, row + 1, 0, counter)
    picture[row][col] = 0
    counter += _helper_how_many_solutions(picture, constraints, row, col + 1, 0)
    picture[row][col] = 1
    counter += _helper_how_many_solutions(picture, constraints, row, col + 1, 0)
    picture[row][col] = -1
    return counter


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """
    This function returns a constraints set for the provided picture, while the picture is its only solution AND every
    constraint in the constraints set is necessary.
    """
    constraints = []
    row_len = len(picture)
    col_len = len(picture[0])
    for row in range(row_len):
        for col in range(col_len):
            constraints.append((row, col, min_seen_cells(picture, row, col)))
    copied = copy.deepcopy(constraints)
    while how_many_solutions(set(copied), row_len, col_len) == 1:
        for constraint in constraints:
            copied = copy.deepcopy(constraints)
            copied.remove(constraint)
            if how_many_solutions(set(copied), row_len, col_len) == 1:
                constraints.remove(constraint)
    return set(constraints)




