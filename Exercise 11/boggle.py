

import boggle_gui
import boggle_model
from constants import *


class BoggleController:

    def __init__(self, time: int, buttons: int):
        """
        A constructor for the Boggle game (creates new game model and graphic).
        :param time: Duration for one game
        :param buttons: A table of buttons in the board.
        """
        self._words = self._create_words_list()
        call = self.check_path
        self._found_words = dict()
        self._model = boggle_model.BoggleModel(self._words, time, buttons)
        self._gui = boggle_gui.BoggleGUI(self._model.get_letters_board(), self._model.get_constants(), call)
        self._score = 0

    def _create_words_list(self) -> Iterable[str]:
        """
        This function gets a file of legal words for the game and creates a words list.
        :return: A list of legal words for the game.
        """
        words = []
        with open('boggle_dict.txt', 'r') as words_file:
            for line in words_file:
                words_split = line.split()
                for word in words_split:
                    words.append(word)
        return words

    def check_path(self):
        """
        This function checks a path after one button is pressed.
        :return: None.
        """
        curr_path = self._gui.get_curr_path()
        text = self._gui.get_text()
        if self._model.is_valid_path(self._model.get_letters_board(), curr_path) is not None and text in self._words:
            word_score = len(curr_path) ** 2
            if text not in self._found_words:
                self._found_words[text] = curr_path[:]
                self._score += word_score
                self._gui.set_menu_labels(text, self._score, word_score)

            elif len(curr_path) > len(self._found_words[text]):
                self._score -= len(self._found_words[text]) ** 2
                self._score += word_score
                self._found_words[text] = curr_path
                self._gui.set_menu_labels(text, self._score, word_score)

    def run(self):
        """
        This function start a new Boggle game (call the constructor of the game controller).
        :return: None.
        """
        restart = self._gui.run()
        if restart:
            BoggleController(180, 16).run()


def main():
    BoggleController(180, 16).run()


if __name__ == "__main__":
    main()
