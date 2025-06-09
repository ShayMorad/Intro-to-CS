

import tkinter as tki
from typing import Dict, Tuple, List, Any
from datetime import datetime
import boggle_board_randomizer
from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]
START_MESSAGE = "Welcome to Boggle by Shay & Shalev!\nPRESS 'START' TO BEGIN"

# STYLING CONSTANTS REGULAR MODE
REGULAR_BUTTON_REGULAR_COLOR = 'ivory3'
REGULAR_BUTTON_ACTIVE_COLOR = 'ivory4'
REGULAR_BUTTON_PRESS_COLOR = 'red3'
REGULAR_MANAGE_BUTTON_COLOR = 'lightgrey'
REGULAR_FRAME_COLOR = 'snow'
REGULAR_OUTER_FRAME_COLOR = 'LavenderBlush2'
REGULAR_FRAME_FOREGROUND = 'black'

# STYLING CONSTANTS DARK MODE
DARK_BUTTON_REGULAR_COLOR = 'gray13'
DARK_BUTTON_ACTIVE_COLOR = 'gray9'
DARK_BUTTON_PRESS_COLOR = 'gray2'
DARK_MANAGE_BUTTON_COLOR = 'lightgrey'
DARK_FRAME_COLOR = 'gray13'
DARK_OUTER_FRAME_COLOR = 'gray2'
DARK_FRAME_FOREGROUND = 'white'

# STYLING CONSTANTS
BUTTON_REGULAR_COLOR = REGULAR_BUTTON_REGULAR_COLOR
BUTTON_ACTIVE_COLOR = REGULAR_BUTTON_ACTIVE_COLOR
BUTTON_PRESS_COLOR = REGULAR_BUTTON_PRESS_COLOR
MANAGE_BUTTON_COLOR = REGULAR_MANAGE_BUTTON_COLOR
FRAME_COLOR = REGULAR_FRAME_COLOR
OUTER_FRAME_COLOR = REGULAR_OUTER_FRAME_COLOR
FONT = ('Helvetica', 30)

CHAR_BUTTON_STYLE = {"font": (FONT, 25),
                     "borderwidth": 3,
                     "relief": tki.RAISED,
                     "bg": BUTTON_REGULAR_COLOR,
                     "activebackground": BUTTON_ACTIVE_COLOR, }
MANAGE_BUTTON_STYLE = {"font": (FONT, 15),
                       "borderwidth": 3,
                       "relief": tki.RAISED,
                       "bg": MANAGE_BUTTON_COLOR,
                       "activebackground": MANAGE_BUTTON_COLOR}

DARK_CHAR_BUTTON_STYLE = {"font": (FONT, 25),
                          "borderwidth": 3,
                          "relief": tki.RAISED,
                          "bg": BUTTON_REGULAR_COLOR,
                          "activebackground": BUTTON_ACTIVE_COLOR,
                          "foreground": "white"}
DARK_MANAGE_BUTTON_STYLE = {"font": (FONT, 15),
                            "borderwidth": 3,
                            "relief": tki.RAISED,
                            "bg": MANAGE_BUTTON_COLOR,
                            "activebackground": MANAGE_BUTTON_COLOR,
                            "foreground": "white"}


def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
