class Car:
    """
    This is a car class ment to be used for the Rush Hour game puzzle game.
    """
    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # if length < 1:
        #     print("Wrong car length, it must be bigger than 0!")
        #     return
        # if orientation not in [1, 0]:
        #     print("Wrong car orientation! Must be 0 for vertical or 1 for horizontal!")
        #     return
        self.__name = str(name)
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = list()
        row, col = self.__location
        if self.__orientation == Car.VERTICAL:
            for row in range(row, row + self.__length):
                coordinates.append((row, col))
        elif self.__orientation == Car.HORIZONTAL:
            for col in range(col, col + self.__length):
                coordinates.append((row, col))
        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car
        """
        possible_moves = dict()
        if self.__orientation == Car.VERTICAL:
            possible_moves["u"] = "Move car up"
            possible_moves["d"] = "Move car down"
        elif self.__orientation == Car.HORIZONTAL:
            possible_moves["l"] = "Move car left"
            possible_moves["r"] = "Move car right"
        return possible_moves

    def movement_requirements(self, move_key):
        """
        :param: move_key: A string representing the key of the required move
        :return: A list of cell locations which must be empty in order for this move to be legal
        """
        car_coordinates = self.car_coordinates()
        if move_key in self.possible_moves().keys():
            if move_key == "u":
                return [(car_coordinates[0][0] - 1, car_coordinates[0][1])]
            elif move_key == "d":
                return [(car_coordinates[-1][0] + 1, car_coordinates[-1][1])]
            elif move_key == "l":
                return [(car_coordinates[0][0], car_coordinates[0][1] - 1)]
            elif move_key == "r":
                return [(car_coordinates[-1][0], car_coordinates[-1][1] + 1)]
        return list()

    def move(self, move_key):
        """ 
        :param: move_key: A string representing the key of the required move
        :return: True upon success, False otherwise
        """
        if move_key in self.possible_moves().keys():
            if move_key == "u":
                self.__location = (self.__location[0] - 1, self.__location[1])
                return True
            elif move_key == "d":
                self.__location = (self.__location[0] + 1, self.__location[1])
                return True
            elif move_key == "l":
                self.__location = (self.__location[0], self.__location[1] - 1)
                return True
            elif move_key == "r":
                self.__location = (self.__location[0], self.__location[1] + 1)
                return True
            return False
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        car_name = self.__name
        return car_name

    def __str__(self):
        """
        :return: Attributes of car.
        """
        if self.__orientation == Car.VERTICAL:
            return f"Name: {self.__name}, length: {self.__length}, location: {self.__location}, " \
                   f"orientation: Vertical"
        elif self.__orientation == Car.HORIZONTAL:
            return f"Name: {self.__name}, length: {self.__length}, location: {self.__location}, " \
                   f"orientation: Horizontal"
        return f"Name: {self.__name}, length: {self.__length}, location: {self.__location}, " \
               f"orientation: {self.__orientation}"

