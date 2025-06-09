from typing import Optional
from game_display import GameDisplay


class SnakeGame:

    def __init__(self, args, board, apples) -> None:
        self.__key_clicked = None
        self.__board = board
        self.__missing_apples = apples
        self.__score = 0

    def read_key(self, key_clicked: Optional[str]) -> None:
        self.__key_clicked = key_clicked

    def update_objects(self):
        self.__board.move_snake(self.__key_clicked)
        if self.__missing_apples > 0:
            if self.__board.add_apple():
                self.__missing_apples -= 1
        if self.__board.check_apple_eaten():
            self.__score += int((self.__board.get_snake().get_snake_length()) ** 0.5)
            self.__missing_apples += 1
        return self.__score

    def draw_board(self, gd: GameDisplay) -> None:
        rows = len(self.__board.get_board())
        cols = len(self.__board.get_board()[0])
        for row_i in range(rows - 1, -1, -1):
            for col_i in range(cols):
                board_cell = self.__board.get_board()[rows - row_i - 1][col_i]
                if board_cell != 0:
                    gd.draw_cell(col_i, row_i, board_cell)

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return self.__board.check_snake_collision()
