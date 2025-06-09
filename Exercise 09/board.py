from car import *

class Board:
    """
    This is a board class ment to be used for the game Rush Hour.
    """
    EXIT = (3, 7)

    def __init__(self):
        """
        Creates an empty board suited for the Rush Hour game.
        """
        self.__board = []
        for row in range(7):
            temp_row = []
            for col in range(8):
                if col == 7 and row == 3:
                    temp_row.append("E")
                elif col == 7 and row != 3:
                    temp_row.append("*")
                else:
                    temp_row.append("_")
            self.__board.append(temp_row)
        self.__cars = []

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_str = ""
        for row in self.__board:
            for col in row:
                board_str += col + " "
            board_str += '\n'
        return board_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cells = []
        for row in range(7):
            for col in range(7):
                cells.append((row, col))
            if row == 3:
                cells.append((3, 7))
        return cells

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        possible_moves = list()
        for car in self.__cars:
            car_possible_moves = car.possible_moves()
            for move, value in car_possible_moves.items():
                must_be_empty_cell_in_board = car.movement_requirements(move)[0]
                if self.cell_content(must_be_empty_cell_in_board) is None:
                    possible_moves.append((car.get_name(), move, value))
        return possible_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3, 7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param: coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate
        if row < 0 or row > 6 or col < 0 or col > 7:
            return False
        if self.__board[row][col] == "_" or self.__board[row][col] == "E":
            return None
        elif self.__board[row][col] != "*":
            return self.__board[row][col]
        elif self.__board[row][col] == "*":
            return False
        return False

    def add_car(self, car):
        """
        Adds a car to the game.
        :param: car: car object of car to add
        :return: True upon success. False if failed
        """
        car_name = car.get_name()
        car_coords = car.car_coordinates()
        for card in self.__cars:
            if car_name == card.get_name():
                return False
        for row in self.__board:
            if car_name in row:
                return False
        for row, col in car_coords:
            if row < 0 or col < 0 or row > 6 or col > 7:
                return False
        for coord in car_coords:
            if self.cell_content(coord) is not None:
                return False
        for row, col in car_coords:
            self.__board[row][col] = car_name
        self.__cars.append(car)
        return True

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param: name: name of the car to move
        :param: move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        can_move = False
        all_possible_moves = self.possible_moves()
        for moveset in all_possible_moves:
            name_possible_car, move_key_possible_car, blank = moveset
            if (name, move_key) == (name_possible_car, move_key_possible_car):
                can_move = True
        if can_move is False:
            return False
        elif can_move is True:
            for car in self.__cars:
                if car.get_name() == name:
                    self.remove_car(car)
                    car.move(move_key)
                    self.__cars.remove(car)
                    self.add_car(car)
                    return True

    def remove_car(self, car):
        """
        :param: car: car to remove from board
        """
        car_coords = car.car_coordinates()
        for row, col in car_coords:
            self.__board[row][col] = "_"

    def get_cars(self):
        cars = []
        for car in self.__cars:
            cars.append(car.__str__())
        return cars


board = Board()
car1 = Car("F1", 2, (3,3), 1)
board.add_car(car1)
print(board)