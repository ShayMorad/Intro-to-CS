from typing import Tuple


class Snake:
    """

    """

    def __init__(self, height: int, width: int):
        self.__row = height // 2
        self.__col = width // 2
        self.__direction = "Up"
        self.__lengthen_snake = 0
        self.__start_length = 3
        self.__cells_list = [(self.__row + i, self.__col) for i in range(self.__start_length)]
        self.__cells_list = self.__cells_list[::-1]

    def move(self):
        """

        :return:
        """
        if self.__direction == "Up":
            self.__row -= 1
        elif self.__direction == "Down":
            self.__row += 1
        elif self.__direction == "Right":
            self.__col += 1
        elif self.__direction == "Left":
            self.__col -= 1
        self.__cells_list.append((self.__row, self.__col))
        if self.__lengthen_snake == 0:
            return self.__cells_list.pop(0), (self.__row, self.__col)
        else:
            self.__lengthen_snake -= 1
            return (-1, -1), (self.__row, self.__col)

    def set_eaten_apple(self, eaten: bool):
        """

        :param eaten:
        :return:
        """
        if eaten:
            self.__lengthen_snake += 3

    def set_direction(self, user_input):
        """

        :param user_input:
        :return:
        """
        if user_input not in ["Right", "Left", "Down", "Up"]:
            return
        if user_input in ["Up", "Down"] and self.__direction in ["Up", "Down"]:
            return
        if user_input in ["Right", "Left"] and self.__direction in ["Right", "Left"]:
            return
        self.__direction = user_input

    def get_snake_cells_list(self):
        return self.__cells_list

    def get_snake_head(self):
        return (self.__row, self.__col)

    def remove_head(self):
        self.__cells_list.pop()

    def get_snake_length(self):
        return len(self.__cells_list)

