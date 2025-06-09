
from constants import *


def _helper_is_empty_board(board: Board) -> bool:
    """
    This helper function checks if the board has no dimensions.
    :param board: The board of the game.
    :return: If board has dimensions --> return True.
             If board has no dimensions --> return False.
    """
    board_height = len(board)
    if board_height < 1:
        return False
    board_width = len(board[0])
    if board_width < 1:
        return False
    return True


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    This function checks whether a given path is valid.
    :param board: The board of the game.
    :param path: A list of tuples of coordinations.
    :param words: The legal words for the game.
    :return: If path is valid --> The word that was found by the path.
             If path is invalid --> None.
    """
    if not _helper_is_empty_board(board):
        return None

    word = ""
    prev = (None, None)
    for coordinate in path:
        if not _helper_is_valid_path(board, prev, coordinate):
            return None
        else:
            row, col = coordinate
            prev = coordinate
            word += board[row][col]

    if word in words:
        return word
    return None


def _helper_is_valid_path(board: Board, prev: Tuple[int, int], coordinate: Tuple[int, int]) -> bool:
    """
    A helper function for the 'is_valid_path' function. Checks whether a coordinate is legal.
    :param board: The board of the game.
    :param prev: Previous coordinate in the path.
    :param coordinate: Current coordinate that is being checked from the path.
    :return: If coordinate is legal --> True.
             If coordinate is illegal --> False.
    """
    board_height, board_width = len(board), len(board[0])
    row, col = coordinate
    if row < 0 or col < 0 or row >= board_height or col >= board_width:
        return False

    # Check for the first coordiante if it's in the board dimensions.
    if prev == (None, None):
        return True

    prev_row, prev_col = prev
    options_list = []
    for i in range(prev_row - 1, prev_row + 2):
        for j in range(prev_col - 1, prev_col + 2):
            if (i, j) != (prev_row, prev_col):
                options_list.append((i, j))

    if (row, col) in options_list:
        return True
    return False


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    This function returns a list of legal path in length of 'n'.
    :param n: The length of paths to check for.
    :param board: The board of the game.
    :param words: The legal words for the game.
    :return: A list of legal paths.
    """
    words = set(words)
    if not _helper_is_empty_board(board):
        return []

    checked_cells = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    paths_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            _helper_find_length_n(board, words, i, j, [], checked_cells, n, paths_list, 'paths')
    paths_list.sort()
    return paths_list


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    This function returns a list of legal path in length of 'n'.
    :param n: The length of paths to check for.
    :param board: The board of the game.
    :param words: The legal words for the game.
    :return: A list of legal paths of words in length 'n'.
    """
    words = set(words)
    if not _helper_is_empty_board(board):
        return []

    checked_cells = [[False for _ in range(len(board[0]))] for _ in range(len(board))]

    paths_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            _helper_find_length_n(board, words, i, j, [], checked_cells, n, paths_list, 'words')
    paths_list.sort()
    return paths_list


def _check_possibility(words: Iterable[str], word_initial: str):
    """
    This function checks if the current word initial can become a full word from the words list.
    :param words: The legal words for the game.
    :param word_initial: A start of a word.
    :return: If word initial can become a full word --> True.
             If word initial can't become a full word --> False.
    """
    for word in words:
        temp_word = word[:len(word_initial)]
        if temp_word == word_initial:
            return True
    return False


def _cut_words_dictionary(words: Iterable[str], path: Path, board: Board) -> Iterable[str]:
    """
    :param words: The board of the game.
    :param path: Current path.
    :param board: The legal words for the game.
    :return: A shorter dictionary that fits better for the current path tree branch.
    """
    current_word = ''
    for coord in path:
        current_word += board[coord[0]][coord[1]]
    cut_words = {word for word in words if
                 word[:len(current_word)] == current_word}
    return cut_words


def _helper_find_length_n(board: Board, words: Iterable[str], row: int, col: int, path: Path,
                          checked_cells: List[List[bool]], n: int, paths_list: List[Path], mode: str) -> None:
    """
    This helper function returns a list of legal paths/words in length of n, using BACKTRACKING.
    :param board: The board of the game.
    :param words: The legal words for the game.
    :param row: Current row index of checked cell.
    :param col: Current col index of checked cell.
    :param path: A list of tuples of coordinations.
    :param checked_cells: A list of boolean values that represents whether the cell was visited.
    :param n: The requested integer to return legal paths by.
    :param paths_list: A list of all legal paths by length of n.
    :param mode: Input 'words' to return paths list of words by len n.
                 Input 'paths' to return paths list of paths by len n.
    :return: Paths list.
    """

    if len(path) == 0:
        path.append((row, col))

    if path.count((row, col)) > 1:
        return

    current_word = ""
    if len(path) > 0:
        for coord in path:
            current_word += board[coord[0]][coord[1]]

        if not _check_possibility(words, current_word):
            return

        iterable_check_len = len(current_word)
        if mode == "paths":
            iterable_check_len = len(path)

        if current_word in words and iterable_check_len == n:
            if path not in paths_list:
                paths_list.append(path)

    options_list = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                options_list.append((row + i, col + j))

    for r, c in options_list:
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and not checked_cells[r][c]:
            checked_cells[r][c] = True
            words = _cut_words_dictionary(words, path, board)
            _helper_find_length_n(board, words, r, c, path + [(r, c)], checked_cells, n, paths_list, mode)
            checked_cells[r][c] = False


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    if not _helper_is_empty_board(board):
        return []


    words = set(words)
    checked_cells = [[False for _ in range(len(board[0]))] for _ in range(len(board))]

    max_n = 0
    for word in words:
        if len(word) >= max_n:
            max_n = len(word)

    words = set(word for word in words if len(word) <= max_n)
    paths_dictionary = dict()

    for i in range(len(board)):
        for j in range(len(board[0])):
            _helper_max_score_paths(board, words, i, j, [], checked_cells, max_n, paths_dictionary)

    max_score_paths_list = []
    for value in paths_dictionary.values():
        max_score_paths_list.append(value)
    return max_score_paths_list


def _helper_max_score_paths(board: Board, words: Iterable[str], row: int, col: int, path: Path,
                            checked_cells: List[List[bool]], max_n: int, paths_dictionary):
    """
    This helper function returns a list of legal paths/words in length of n, using BACKTRACKING.
    :param board: The board of the game.
    :param words: The legal words for the game.
    :param row: Current row index of checked cell.
    :param col: Current col index of checked cell.
    :param path: A list of tuples of coordinations.
    :param checked_cells: A list of boolean values that represents whether the cell was visited.
    :param max_n: The requested integer to return legal paths by.
    :param paths_dictionary: A dictionary of all legal paths by length of n of existing words in the words file.
    :return: Paths list.
    """
    words = _cut_words_dictionary(words, path, board)
    current_word = ""
    if len(path) > 0:
        for coord in path:
            current_word += board[coord[0]][coord[1]]

        if not _check_possibility(words, current_word):
            return

        if current_word in words and len(path) <= max_n:
            if current_word not in paths_dictionary.keys():
                paths_dictionary[current_word] = path
            elif len(path) > len(paths_dictionary[current_word]):
                paths_dictionary[current_word] = path

    options_list = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                options_list.append((row + i, col + j))

    for r, c in options_list:
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and not checked_cells[r][c]:
            checked_cells[r][c] = True
            words = _cut_words_dictionary(words, path, board)
            _helper_max_score_paths(board, words, r, c, path + [(r, c)], checked_cells, max_n, paths_dictionary)
            checked_cells[r][c] = False


