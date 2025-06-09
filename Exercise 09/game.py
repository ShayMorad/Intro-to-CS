from board import *
from car import *
from helper import *
import sys


class Game:
    """
    This is a game class based on the board and car classses that initializes a game object for the Rush Hour game.
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param: board: An object of type board
        """
        self.__board = board
        self.game_on = True

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        #Before and after every stage of a turn, you may print additional
        #information for the user, e.g., printing the board. In particular,
        #you may support additional features, (e.g., hints) as long as they
        #don't interfere with the API.
        """
        print()
        print(self.__board)
        print(f"These are the possible moves for the cars on the board: {self.__board.possible_moves()}.")
        if self.__board.cell_content(self.__board.target_location()) is not None:
            print("Congratulations!")
            self.game_on = False
            return
        user_input = input(
            "Please insert which car you want to move by the following format: 'name','direction'. "
            "If you want to exit the game, insert: '!' : ")
        print()
        if self.__board.cell_content(self.__board.target_location()) is not None:
            print("Congratulations!")
            self.game_on = False
            return
        if user_input == "!":
            print("Closing game...")
            self.game_on = False
            return
        if "," not in user_input:
            print()
            print("Wrong format, please try again.\n")
            return
        elif "," in user_input:
            if user_input.count(',') != 1:
                print()
                print("Wrong format, please try again. \n")
                return
            else:
                user_choices = user_input.split(",")
                car_name = user_choices[0]
                car_direction = user_choices[1]
                move_car = self.__board.move_car(car_name, car_direction)
                if move_car is True:
                    print("The car was moved.")
                    if self.__board.cell_content(self.__board.target_location()) is not None:
                        print("Congratulations! You have won the game!")
                        self.game_on = False
                        return
                    return
                else:
                    print("Can't move car! Wrong format!")
                    return

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print("Welcome to Shayke's Rush-Hour game!\n")
        while self.game_on:
            self.__single_turn()

def json_to_list(path):
    car_configuration = load_json(path)
    listed_car_config = []
    for key in car_configuration.keys():
        temp = [key]
        for items in car_configuration[key]:
            if isinstance(items, list):
                temp.append((items[0], items[1]))
            else:
                temp.append(items)
        listed_car_config.append(temp)
    return listed_car_config

def car_checks(car_information):
    CAR_NAMES = ['Y', 'B', 'O', 'G', 'W', 'R']
    car_name = car_information[0]
    car_length = car_information[1]
    car_orientation = car_information[3]
    if car_name not in CAR_NAMES:
        return False
    if car_length < 2 or car_length > 4:
        return False
    if car_orientation not in [0, 1]:
        return False
    return True

def create_car_from_car_information(car_information):
    car_name = car_information[0]
    car_length = car_information[1]
    car_coord = car_information[2]
    car_orientation = car_information[3]
    new_car = Car(car_name, car_length, car_coord, car_orientation)
    return new_car

if __name__ == "__main__":
    board1 = Board()
    listed_car_config = json_to_list(sys.argv[1])
    for car_information in listed_car_config:
        if car_checks(car_information):
            car = create_car_from_car_information(car_information)
            board1.add_car(car)
    game1 = Game(board1)
    game1.play()
