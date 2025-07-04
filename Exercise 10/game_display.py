import sys,getopt
import threading
import time
import tkinter as tki
from typing import Any, Optional, List, Tuple, Dict

import argparse
from argparse import Namespace

import game_utils

CELL_SIZE = 15
ROUND_TIME = 100

WIDTH = 40
HEIGHT = 30
NUM_OF_APPLES = 3
NUM_OF_WALLS = 2

class GameDisplay:
    def __init__(self, width:int, height:int, delay:int, verbose:int, args:Namespace) -> None:
        """Creates a new game display object and initializes it"""
        # placed this import in here to solve circular import issues.
        self.width, self.height, self.delay, self.verbose = width, height, delay/1000, verbose>1
        import snake_main
        self._round_num = 0
        self._root = tki.Tk()
        self._root.title('Snake')
        self._root.bind('<KeyPress>', self._key_press)

        self._score_var = tki.StringVar()

        self._init_score_frame()
        self._canvas = tki.Canvas(
            self._root, bg="white", width = self.width * CELL_SIZE,
            height = self.height * CELL_SIZE)
        self._canvas.pack()
        self._to_draw: Dict[Tuple[int, int], str] = dict()
        self._already_drawn: Dict[Tuple[int, int, str], int] = dict()

        self._root.resizable(False, False)
        self.key_click: Optional[str] = None
        self._key_click_round: int = 0

        self._game_control_thread = threading.Thread(
            target=snake_main.main_loop, args=(self,args))
        self._game_control_thread.daemon = True
        self._round_start_time = time.time()



    def _init_score_frame(self) -> None:
        """
        Internal: This method initializes the score frame
        :return: None
        """
        self._score_frame = tki.Frame(self._root)
        self._score_frame.pack(side=tki.TOP)

        self.show_score("Not Set")
        self._score_label = tki.Label(self._score_frame,
                                      borderwidth=2,
                                      relief="ridge",
                                      textvariable=self._score_var,
                                      font=("Courier", 22))

        self._score_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self._score_frame.grid_rowconfigure(0, weight=1)

    def start(self) -> None:
        """
        Internal: Starts the program: calls the main method and runs the GUI.
        :return: None
        """
        self._root.after(500, self._game_control_thread.start)
        self._root.after(1000, self._check_end)

        self._root.mainloop()

    def _check_end(self) -> None:
        """
        Internal: This methods checks if the game has finished
        :return: None
        """
        if not self._game_control_thread.is_alive():
            self._root.after(1000, self._root.destroy)
        else:
            self._root.after(300, self._check_end)

    def _key_press(self, e: Any) -> None:
        """
        Internal: checks which key was clicked in the event
        :param e:event
        :return:None
        """
        if e.keysym in ["Left", "Right", "Up", "Down"]:
            self.key_click = e.keysym
            self._key_click_round = self._round_num

    def get_key_clicked(self) -> Optional[str]:
        """
        This method returns which key is clicked
        and also turns off the key clicked FLAG
        :return: None, or one of 'Left', 'Right', 'Up', 'Down'
        """
        result = self.key_click
        self.key_click = None
        return result

    def draw_cell(self, x: int, y: int, color: str) -> None:
        """
        Sets the cell at the given coordinates to draw in given color
        :param x: coordinate at x
        :param y: coordinate at y
        :param color: the color we wish to draw
        :return: None
        """
        self._to_draw[x, y] = color

    def _buffer_draw_cell(self, x: int, y: int, color: str) -> int:
        """
        Internal: internal method to draw the x,y cell in color
        :param x: coordinate at x
        :param y: coordinate at y
        :param color: the color we wish to draw
        :return: None
        """
        if x < 0 or x >= self.width or \
                y < 0 or y >= self.height:
            raise ValueError(
                "cell index out of bounds of the board: " + str((x, y)))

        # setting the coordinates of the board correctly,
        # the y axis needs to point up.
        # the following line adjusts this.
        y = self.height - y
        return self._canvas.create_rectangle(
            x * CELL_SIZE, (y - 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
            y * CELL_SIZE,
            fill=color, outline=color)

    def _update_drawing(self) -> None:
        """
        Internal: method to update drawing
        :return: None
        """
        if self.verbose:
            print(self._to_draw)
        to_draw = {(x,y,color) for (x,y),color in self._to_draw.items()}
        for rect in self._already_drawn:
            if rect not in to_draw:
                self._canvas.delete(self._already_drawn[rect])

        cur_drawn: Dict[Tuple[int, int, str], int] = dict()
        for (x, y), color in self._to_draw.items():
            ind = self._already_drawn.get((x, y, color), None)
            if ind is None:
                ind = self._buffer_draw_cell(x, y, color)
            cur_drawn[(x, y, color)] = ind

        self._already_drawn = cur_drawn
        self._to_draw = dict()

    def end_round(self) -> None:
        """
        This method ends the current round.
        :return:None
        """
        self._update_drawing()

        self._round_start_time += self.delay
        now = time.time()
        while now < self._round_start_time:
            time.sleep(self._round_start_time - now)
            now = time.time()
        self._round_num += 1

    def show_score(self, val: Any) -> None:
        """
        This method updates the currently shown score on the board.
        :param val: the score we wish to display
        :return: None
        """
        if self.verbose:
            print(f'Score:{val}')
        self._score_var.set("Score: " + str(val))


def parse_args(argv:List[str])->Namespace:
    parser = argparse.ArgumentParser(
        prog = 'game_display.py',
        description = 'Runs snake game',
    )
    parser.add_argument('-x', '--width', type=int, default=WIDTH,
                        help='args.width: Game board width')
    parser.add_argument('-y', '--height', type=int, default=HEIGHT,
                        help='args.height: Game board height')
    parser.add_argument('-s', '--seed', default=None,
                        help='Seed for random number generator (not passed to game loop)')
    parser.add_argument('-a', '--apples', type=int, default=NUM_OF_APPLES,
                        help='args.apples: Number of apples')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='args.debug: Debug mode with no snake')
    parser.add_argument('-w', '--walls', type=int, default=NUM_OF_WALLS,
                        help='args.walls: Number of walls')
    parser.add_argument('-r', '--rounds', type=int, default=-1,
                        help='args.rounds: Number of rounds')
    parser.add_argument('-t', '--delay', type=int, default=ROUND_TIME,
                        help='Delay between rounds in milliseconds (not passed to game loop)')
    parser.add_argument('-v', '--verbose',
                        action='count', default=0,
                        help='Print helpful debugging information (not passed to game loop, can be used multiple times)')
    return parser.parse_args(argv)


def setup_game(args:Namespace)->GameDisplay:
    game_utils.set_random_seed(args.__dict__.pop('seed'))
    game_utils.set_verbose(args.verbose)
    game_utils.set_size(width=args.width,
                              height=args.height)
    return GameDisplay(width=args.width,
                       height=args.height,
                       delay=args.__dict__.pop('delay'),
                       verbose=args.__dict__.pop('verbose'),
                       args=args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    gd = setup_game(args)
    gd.start()
