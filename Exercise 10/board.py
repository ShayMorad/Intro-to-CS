import game_display
import game_utils


class Board:
    """

    """

    def __init__(self, height=30, width=40):
        self.__width = width
        self.__height = height
        self.__snake = None
        self.__board = []
        for row in range(self.__height):
            self.__board.append([0 for c in range(self.__width)])
        self.__apples_list = []

    def __str__(self):
        string = ""
        for row in self.__board:
            for col in row:
                string += str(col) + " "
            string += "\n"
        return string

    def add_snake(self, snake):
        self.__snake = snake
        if self.__height < 3 or self.__width < 1:
            return False
        for cell in self.__snake.get_snake_cells_list():
            row, col = cell
            self.__board[row][col] = "black"

    def move_snake(self, user_input):
        self.__snake.set_direction(user_input)
        snake_tail, snake_head = self.__snake.move()
        if snake_tail != (-1, -1):
            row, col = snake_tail
            self.__board[row][col] = 0
        row, col = snake_head
        if row >= len(self.__board) or row < 0 or col < 0 or col >= len(self.__board[0]):
            return
        self.__board[row][col] = 'black'

    def check_snake_collision(self):
        """
        This function checks weather there was a collision of the snake with a hard entity
        :return:
        """
        snake_cells = self.__snake.get_snake_cells_list()
        snake_row, snake_col = self.__snake.get_snake_head()
        for cell in snake_cells:
            if snake_cells.count(cell) > 1:
                self.__snake.remove_head()
                return True
        if 0 <= snake_row < self.__height and 0 <= snake_col < self.__width:
            return False
        else:
            self.__snake.remove_head()
            return True

    def add_apple(self) -> bool:
        col, row = game_utils.get_random_apple_data()
        row = self.__height - row - 1
        if self.__board[row][col] == 0:
            self.__board[row][col] = 'green'
            self.__apples_list.append((row, col))
            return True
        return False

    def check_apple_eaten(self):
        for apple_cell in self.__apples_list:
            if self.__snake.get_snake_head() == apple_cell:
                self.__snake.set_eaten_apple(True)
                self.__apples_list.remove(apple_cell)
                return True
        return False

    def add_wall(self, wall):
        pass

    def get_board(self):
        return self.__board

    def get_snake(self):
        return self.__snake
