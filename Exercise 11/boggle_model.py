

import ex11_utils
from constants import *
import ex11_utils


class BoggleModel:

    def __init__(self, words: Iterable[str], time: int, buttons: int):
        """
        A constructor for the Boggle model.
        :param words: The legal words for the game.
        :param time: Duration for one game
        :param buttons: A table of buttons in the board.
        """
        self._words = words
        self._time = time
        self._buttons = buttons
        self._letters_board = boggle_board_randomizer.randomize_board()

    def is_valid_path(self, board: Board, path: Path) -> Optional[str]:
        """
        This function checks whether a path on the board is valid.
        :param board: The board of the game.
        :param path: A list of tuples of coordinations.
        :return: If path is valid --> The word that was found by the path.
                 If path is invalid --> None.
        """
        return ex11_utils.is_valid_path(board, path, self._words)

    def get_letters_board(self):
        """
        A getter function of the game's board.
        :return: The board of the game.
        """
        return self._letters_board

    def get_time(self):
        """
        A getter function of the game's duration.
        :return: The duration of the game.
        """
        return self._time

    def get_constants(self):
        """
        A getter function of the game's constants (time, size).
        :return: The constants of the game.
        """
        return self._time, int(self._buttons ** 0.5), int(self._buttons ** 0.5)


def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
