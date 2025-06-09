import copy

import helper


def init_board(rows, columns):
    """Initialize a board based on rows and columns entered."""
    board = []
    for row in range(rows):
        temp_row = []
        for column in range(columns):
            temp_row.append(helper.WATER)
        board.append(temp_row)
    return board


def cell_loc(loc):
    """Decrypt a string coordinate 'XN' to a tuple coordinate (x,y)"""
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    row_index = int(loc[1:]) - 1
    column_index = ord(loc[0]) - 65

    # rows = [str(num) for num in range(helper.NUM_ROWS)]
    # columns = letters[:helper.NUM_COLUMNS]
    # if float(loc[1:]) > 99:
    #    return None
    # elif float(loc[1:]) > helper.NUM_ROWS:
    #    return None

    if helper.is_int(loc[1:]) == False:
        return None
    elif loc[0:1] not in letters:
        return None
    elif loc[0] in letters and (int(loc[1:]) - 1) <= 98:
        return (row_index, column_index)
    else:
        return None


def valid_ship(board, size, loc):
    """Checks if a ship can be placed on a given coordinate on a given board. The placement is vertical on the board."""
    board_column_length = len(board)
    row_index, column_index = loc
    last_ship_row = row_index + size

    if size > board_column_length:
        return False
    elif (board_column_length - row_index) < size:
        return False
    elif size <= board_column_length and (board_column_length - row_index) >= size:
        for row in board[row_index:last_ship_row]:
            if row[column_index] != helper.WATER:
                return False
        return True
    else:
        return False


def create_player_board(rows, columns, ship_sizes):
    """Create a board and place ships based on user input, ships sizes parameter and rows and columns parameters."""
    board = init_board(rows, columns)
    for ship_size in ship_sizes:
        valid_ship_placement = False
        valid_input = False
        helper.print_board(board)

        while valid_input == False:
            user_input = helper.get_input(f"Please pick top coordinate to place a ship of size {ship_size}: ")
            user_input = user_input.upper()
            if user_input == "":
                valid_input = False
                print('Wrong input, you did not enter a correct value.')
            elif " " in user_input:
                valid_input = False
                print('Wrong input, you did not enter a correct column value.')
                helper.print_board(board)
            elif user_input[0] not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:columns]):
                valid_input = False
                print('Wrong input, you did not enter a correct column value.')
                helper.print_board(board)
            elif helper.is_int(user_input[1:]) == False:
                valid_input = False
                print('Wrong input, you did not enter a correct row value.')
                helper.print_board(board)
            elif int(user_input[1:]) > rows or int(user_input[1:]) < 1:
                valid_input = False
                print('Wrong input, you did not enter a correct row value.')
                helper.print_board(board)
            elif user_input[0] in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:columns]) and (
                    int(user_input[1:]) <= rows or int(user_input[1:]) > 0):
                valid_input = True
                ship_placement = cell_loc(user_input)

        while valid_ship_placement == False:
            valid_ship_placement = valid_ship(board, ship_size, ship_placement)
            if valid_ship_placement:
                row_placement, column_placement = ship_placement
                for row in board[row_placement:(row_placement + ship_size)]:
                    row[column_placement] = helper.SHIP
            else:
                print()
                print("********** Out of bounds or collision, try again. **********")
                while True:
                    helper.print_board(board)
                    user_input = helper.get_input(f"Please pick top coordinate to place a ship of size {ship_size}: ")
                    user_input = user_input.upper()

                    if user_input == "":
                        valid_input = False
                        print('Wrong input, you did not enter a correct value.')

                    elif " " in user_input:
                        valid_input = False
                        print('Wrong input, you did not enter a correct column value.')


                    elif helper.is_int(user_input[1:]) == False:
                        valid_input = False
                        print('Wrong input, you did not enter a correct row value.')


                    elif int(user_input[1:]) > rows or int(user_input[1:]) < 1:
                        valid_input = False
                        print('Wrong input, you did not enter a correct row value.')


                    elif user_input[0] not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:columns]):
                        valid_input = False
                        print('Wrong input, you did not enter a correct column value.')


                    elif user_input[0] in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:columns]) and (
                            int(user_input[1:]) <= rows or int(user_input[1:]) > 0):
                        valid_input = True
                        ship_placement = cell_loc(user_input)
                        break
    return board


def fire_torpedo(board, loc):
    """Fires torpedo on the board with a given coordiante after it was decrypted using cell_loc function.
    If water was hit, the coordinate will be change to a hit water.
    If ship was hit, the coordinate will be change to a hit ship."""
    row_coor, column_coor = loc
    target = board[row_coor][column_coor]
    if target == helper.WATER:
        board[row_coor][column_coor] = helper.HIT_WATER
    elif target == helper.SHIP:
        board[row_coor][column_coor] = helper.HIT_SHIP
    return board


def main():
    ### GAME RUNS ####################################################
    playon = True
    while playon:
        ######### CREATE BOARDS
        user_board = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS, helper.SHIP_SIZES)
        pc_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
        hidden_board = copy.deepcopy(pc_board)
        hidden_user_board = copy.deepcopy(hidden_board)

        ###CHECK AVAILABLE SHIP LOCATIONS FOR PC
        all_water_indexes = set()
        for row_index in range(len(pc_board)):
            tile_index = 0
            for tile in pc_board[row_index]:
                if tile == helper.WATER:
                    all_water_indexes.add((row_index, tile_index))
                tile_index += 1

        ### PICK LOCATION, CHECK IF VALID AND UPDATE PC BOARD
        available_indexes_for_pc_ship = all_water_indexes
        ship_sizes = []
        for size in helper.SHIP_SIZES:
            ship_sizes.append(size)
        while len(ship_sizes) > 0:
            to_remove_from_available_locations = []

            for location in available_indexes_for_pc_ship:
                is_rand_loc_valid = valid_ship(pc_board, ship_sizes[0], location)
                if is_rand_loc_valid == False:
                    to_remove_from_available_locations.append(location)

            for item in to_remove_from_available_locations:
                available_indexes_for_pc_ship.remove(item)

            rand_pc_loc = helper.choose_ship_location(pc_board, ship_sizes[0], available_indexes_for_pc_ship)
            is_rand_loc_valid = valid_ship(pc_board, ship_sizes[0], rand_pc_loc)

            if is_rand_loc_valid == True:
                row_placement, column_placement = rand_pc_loc
                for row in pc_board[row_placement:(row_placement + ship_sizes[0])]:
                    row[column_placement] = helper.SHIP
                ship_sizes.pop(0)
                available_indexes_for_pc_ship.remove(rand_pc_loc)
            else:
                available_indexes_for_pc_ship.remove(rand_pc_loc)
                continue

        #######PRINT BOARDS
        helper.print_board(user_board, hidden_board)

        ######SHOOT USER TORPEDO
        valid_input = False
        while valid_input == False:
            user_torpedo = helper.get_input("Choose a location to shoot your torpedo: ")
            user_torpedo = user_torpedo.upper()
            if user_torpedo == "":
                valid_input = False
                print('Wrong input, you did not enter a correct value.')
            elif " " in user_torpedo:
                valid_input = False
                print('Wrong input, you did not enter a correct column value.')
            elif user_torpedo[0] not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(user_board[0])]):
                valid_input = False
                print('Wrong input, you did not enter a correct column value.')
            elif helper.is_int(user_torpedo[1:]) == False:
                valid_input = False
                print('Wrong input, you did not enter a correct row value.')
            elif " " in user_torpedo:
                valid_input = False
                print('Wrong input, you did not enter a correct column value.')
            elif int(user_torpedo[1:]) > (len(user_board)) or int(user_torpedo[1:]) < 1:
                valid_input = False
                print('Wrong input, you did not enter a correct row value.')
            elif user_torpedo[0] in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(user_board[0])]) and (
                    int(user_torpedo[1:]) <= (len(user_torpedo)) or int(user_torpedo[1:]) > 0):
                valid_input = True
        user_torpedo_loc = cell_loc(user_torpedo)
        fire_torpedo(pc_board, user_torpedo_loc)

        ###UPDATE HIDDEN BOARD

        hidden_board = copy.deepcopy(pc_board)
        for row_index in range(len(hidden_board)):
            tile_index = 0
            for tile in hidden_board[row_index]:
                if tile == helper.SHIP:
                    hidden_board[row_index][tile_index] = helper.WATER
                tile_index += 1

        #### AVAILABLE TORPEDO LOCATIONS FOR PC
        available_indexes_for_pc_torpedo = set()
        for row_index in range(len(user_board)):
            tile_index = 0
            for tile in user_board[row_index]:
                if tile == helper.WATER or tile == helper.SHIP:
                    available_indexes_for_pc_torpedo.add((row_index, tile_index))
                tile_index += 1

        ##### PC TORPEDO SHOT
        random_pc_torpedo = helper.choose_torpedo_target(hidden_user_board, available_indexes_for_pc_torpedo)
        fire_torpedo(user_board, random_pc_torpedo)

        #### UPDATE USER HIDDEN BOARD
        hidden_user_board = copy.deepcopy(user_board)
        for row_index in range(len(hidden_user_board)):
            tile_index = 0
            for tile in hidden_user_board[row_index]:
                if tile == helper.SHIP:
                    hidden_user_board[row_index][tile_index] = helper.WATER
                tile_index += 1

        helper.print_board(user_board, hidden_board)

        #######is game finished? #############################################
        game_finished = False
        while game_finished == False:
            # check if game finished
            game_finished = True
            for list in pc_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! The user have won!")
                break
            game_finished = True
            for list in user_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! PC have won!")
                break

            ###USER TORPEDO
            valid_input = False
            while valid_input == False:
                user_torpedo = helper.get_input("Choose a location to shoot your torpedo: ")
                user_torpedo = user_torpedo.upper()
                if user_torpedo == "":
                    valid_input = False
                    print('Wrong input, you did not enter a correct value.')
                elif user_torpedo[0] not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(user_board[0])]):
                    valid_input = False
                    print('Wrong input, you did not enter a correct column value.')
                elif helper.is_int(user_torpedo[1:]) == False:
                    valid_input = False
                    print('Wrong input, you did not enter a correct row value.')
                elif int(user_torpedo[1:]) > (len(user_board)) or int(user_torpedo[1:]) < 1:
                    valid_input = False
                    print('Wrong input, you did not enter a correct row value.')
                elif " " in user_torpedo:
                    valid_input = False
                    print('Wrong input, you did not enter a correct column value.')
                elif user_torpedo[0] in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(user_board[0])]) and (
                        int(user_torpedo[1:]) <= (len(user_torpedo)) or int(user_torpedo[1:]) > 0):
                    valid_input = True
                    user_torpedo_loc = cell_loc(user_torpedo)
                    if (pc_board[user_torpedo_loc[0]][user_torpedo_loc[1]] == helper.HIT_WATER) or (
                            pc_board[user_torpedo_loc[0]][user_torpedo_loc[1]] == helper.HIT_SHIP):
                        valid_input = False
                        print("You have chosen a location that was already shot, please choose a valid location.")
                    else:
                        user_torpedo_loc = cell_loc(user_torpedo)
                        valid_input = True

            fire_torpedo(pc_board, user_torpedo_loc)
            hidden_board = copy.deepcopy(pc_board)
            for row_index in range(len(hidden_board)):
                tile_index = 0
                for tile in hidden_board[row_index]:
                    if tile == helper.SHIP:
                        hidden_board[row_index][tile_index] = helper.WATER
                    tile_index += 1

            #### PC TORPEDO
            available_indexes_for_pc_torpedo = set()
            for row_index in range(len(user_board)):
                tile_index = 0
                for tile in user_board[row_index]:
                    if tile == helper.WATER or tile == helper.SHIP:
                        available_indexes_for_pc_torpedo.add((row_index, tile_index))
                    tile_index += 1

            ##### PC SHOOT TORPEDO
            random_pc_torpedo = helper.choose_torpedo_target(hidden_user_board, available_indexes_for_pc_torpedo)
            fire_torpedo(user_board, random_pc_torpedo)
            # check if game finished
            game_finished = True
            for list in pc_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! The user have won!")
                break
            game_finished = True
            for list in user_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! PC have won!")
                break
            #### UPDATE USER HIDDEN BOARD
            hidden_user_board = copy.deepcopy(user_board)
            for row_index in range(len(hidden_user_board)):
                tile_index = 0
                for tile in hidden_user_board[row_index]:
                    if tile == helper.SHIP:
                        hidden_user_board[row_index][tile_index] = helper.WATER
                    tile_index += 1

            helper.print_board(user_board, hidden_board)

            ################ CHECK FOR TIE
            game_finished = True
            for list in pc_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                for list in user_board:
                    if helper.SHIP in list:
                        game_finished = False
                if game_finished:
                    helper.print_board(user_board, pc_board)
                    # print("The game is over! It's a Tie!")
                    break
            ################ CHECK FOR USER WIN
            game_finished = True
            for list in pc_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! The user have won!")
                break
            ################ CHECK FOR PC WIN
            game_finished = True
            for list in user_board:
                if helper.SHIP in list:
                    game_finished = False
            if game_finished:
                helper.print_board(user_board, pc_board)
                # print("The game is over! PC have won!")
                break
        ################### PLAY ON?
        while True:
            play_on = helper.get_input("Play again? Enter Y/N: ")
            if play_on == "Y":
                playon = True
                break
            elif play_on == "N":
                playon = False
                break
            else:
                print("Incorrect value, please enter 'Y' or 'N'.")
                play_on = helper.get_input("Play again? Enter Y/N: ")


if __name__ == "__main__":
    main()
