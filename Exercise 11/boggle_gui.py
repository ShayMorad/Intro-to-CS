


import tkinter
import boggle

from constants import *


class BoggleGUI:
    _chars_buttons: Dict[Tuple[int, int], tki.Button] = {}
    _management_buttons: Dict[str, tki.Button or tki.Checkbutton] = {}

    def __init__(self, letters_board, constants: Tuple, func) -> None:
        """
        A constructor for the Boggle model.
        :param letters_board: The board of the game.
        :param constants: The game's constants (time, size).
        :param func: A linking function to the game model.
        """
        self._call = func
        root = tki.Tk()
        root.title("BOGGLE by Shay&Shalev")
        root.resizable(False, False)
        self._main_window = root
        self._letters_board = letters_board
        self._duration_time, self._buttons_rows, self._buttons_cols = constants
        self._save_time = self._duration_time
        self._score_dict = dict()
        self._restart = False

        # initializing the outer frame
        self._outer_frame = tki.Frame(root, bg=OUTER_FRAME_COLOR, highlightbackground=OUTER_FRAME_COLOR,
                                      highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # initializing the top frame
        self._top_frame = tki.Frame(self._outer_frame, bg=OUTER_FRAME_COLOR, highlightbackground=OUTER_FRAME_COLOR,
                                    highlightthickness=2)
        self._top_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        minutes = self._duration_time // 60
        if minutes < 10:
            minutes = "0" + str(minutes)
        seconds = self._duration_time % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        time = f"{minutes}:{seconds}"

        # initializing the clock label
        self._clock_label = tki.Label(self._top_frame, font=FONT, bg=FRAME_COLOR, height=2,
                                      relief=tki.SUNKEN, borderwidth=1, text=time)
        self._clock_label.grid(row=0, column=0, padx=1, sticky='nsew')

        # initializing the score label
        self._score_label = tki.Label(self._top_frame, padx=1, font=FONT, bg=FRAME_COLOR, height=2,
                                      relief=tki.SUNKEN, borderwidth=1, text='Score: 0')
        self._score_label.grid(row=0, column=1, padx=1, sticky='nsew')

        # initializing the display line
        self._display_line = tki.Label(self._top_frame, text=START_MESSAGE, pady=1, font=FONT, bg=FRAME_COLOR, height=2,
                                       relief=tki.SUNKEN)
        self._display_line.grid(columnspan=2, row=1, pady=1, sticky='nsew')

        self._top_frame.grid_columnconfigure(0, weight=1)
        self._top_frame.grid_columnconfigure(1, weight=1)
        self._top_frame.grid_rowconfigure(1, weight=1)

        # initializing the center frame
        self._center_frame = tki.Frame(self._outer_frame)
        self._center_frame.pack(fill=tki.BOTH, expand=True)

        # initializing the buttons frame and adding chars buttons
        self._buttons_frame = tki.Frame(self._center_frame)
        self._buttons_frame.pack(side=tki.LEFT, fill=tki.BOTH, expand=True)
        self._create_buttons_in_chars_frame(self._letters_board)

        self._cover_frame = tki.Frame(self._buttons_frame, bg='gray', width=200, height=200)
        self._cover_frame.grid(row=0, column=0, rowspan=len(self._letters_board),
                               columnspan=len(self._letters_board[0]),
                               sticky='nsew')
        self._cover_frame.lift()

        # initializing the right frame
        self._right_frame = tki.Frame(self._center_frame)
        self._right_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)
        self._create_scrollbar()

        # initializing the bottom frame and adding managements buttons
        self._bottom_frame = tki.Frame(self._outer_frame)
        self._bottom_frame.grid_columnconfigure(0, weight=1)
        self._bottom_frame.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)
        self._create_managements_buttons()

        self._main_window.bind("<ButtonRelease-1>", self._button_pressed)
        self._text = ''
        self._pressed_buttons = []
        self._dark_status = 0

    def _create_buttons_in_chars_frame(self, letters_board: List[List[str]]) -> None:
        """
        This function creates the letters buttons in the center frame.
        :param letters_board: The board of the game.
        :return: None
        """
        for row in range(self._buttons_rows):
            for col in range(self._buttons_cols):
                str_display = letters_board[row][col]
                self._create_char_button(str_display, row, col)

    def _create_char_button(self, str_display: str, row: int, col: int) -> tki.Button:
        """
        This function creates a letter button and places it in the center frame.
        :param str_display: The button display
        :param row: The row of the button in the board.
        :param col: The column of the button in the board.
        :return: A letter button.
        """
        button = tki.Button(self._buttons_frame, height=2, width=6, text=str_display, **CHAR_BUTTON_STYLE)
        button.grid(row=row, column=col)
        self._chars_buttons[(row, col)] = button

        def _on_enter(event: Any) -> None:
            pass

        def _on_leave(event: Any) -> None:
            pass

        def _on_press(event: Any) -> None:
            options_list = []
            if len(self._pressed_buttons) > 0:
                last_pressed_button = self._pressed_buttons[-1]
                last_row, last_col = last_pressed_button
                for i in range(last_row - 1, last_row + 2):
                    for j in range(last_col - 1, last_col + 2):
                        if (i, j) != (last_row, last_col):
                            options_list.append((i, j))
            if len(self._pressed_buttons) == 0 or (row, col) in options_list:
                if (row, col) in self._pressed_buttons:
                    # button['activebackground'] = BUTTON_PRESS_COLOR
                    button['background'] = BUTTON_PRESS_COLOR
                else:
                    # button['activebackground'] = BUTTON_PRESS_COLOR
                    button['background'] = BUTTON_PRESS_COLOR
                    self._pressed_buttons.append((row, col))
                    self._text += button['text']
            self._call()

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.bind('<ButtonRelease-1>', _on_press)

        return button

    def _create_managements_buttons(self) -> None:
        """
        This function creates and places the menu buttons (start, delete, quit, dark mode).
        :return: None.
        """
        dark_mode_button = tki.Checkbutton(self._bottom_frame, text="DARK MODE", onvalue=1, offvalue=0,
                                           command=self._dark_mode, font=(FONT, 13))
        start_button = tki.Button(self._bottom_frame, height=1, width=7, text="START", command=self._update_time,
                                  **MANAGE_BUTTON_STYLE)
        delete_button = tki.Button(self._bottom_frame, height=1, width=7, text="DELETE", command=self._clear_display,
                                   **MANAGE_BUTTON_STYLE)
        quit_button = tki.Button(self._bottom_frame, height=1, width=7, text="QUIT", command=self.quit,
                                 **MANAGE_BUTTON_STYLE)

        dark_mode_button.grid(row=0, column=0, sticky=tki.W)
        start_button.grid(row=0, column=1, sticky=tki.E)
        delete_button.grid(row=0, column=2, sticky=tki.E)
        quit_button.grid(row=0, column=3, sticky=tki.E)

        self._management_buttons["dark_mode"] = dark_mode_button
        self._management_buttons["start button"] = start_button
        self._management_buttons["quit button"] = quit_button

    def _create_scrollbar(self):
        """
        This function creates the found words label and the scrollbar.
        :return: None.
        """
        self._text_label = tki.Text(self._right_frame, width=15, height=3, font=FONT, state=tki.DISABLED)
        scrollbar = tki.Scrollbar(self._right_frame, orient=tki.VERTICAL, command=self._text_label.yview)
        self._text_label.config(yscrollcommand=scrollbar.set)
        self._text_label.pack(side=tki.LEFT, anchor='w', fill='y')
        scrollbar.pack(side=tki.RIGHT, anchor='e', fill='y')

    def run(self) -> bool:
        """
        This function runs the graphic model of the Boggle game.
        :return: A boolean variable about game restart.
        """
        self._main_window.mainloop()
        return self._restart

    def quit(self):
        """
        This function quits the graphic model of the Boggle game.
        :return: None.
        """
        self._main_window.destroy()

    def empty(self):
        return None

    def _update_time(self) -> None:
        """
        This function create the game timer and updates its.
        :return: None
        """
        self._cover_frame.grid_remove()
        self._management_buttons["start button"]["command"] = self.empty

        minutes = self._duration_time // 60
        if minutes < 10:
            minutes = "0" + str(minutes)
        seconds = self._duration_time % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        self._clock_label.configure(text=f"{minutes}:{seconds}")

        self._duration_time -= 1

        if self._duration_time >= 0:
            self._after_main = self._main_window.after(1000, self._update_time)
        else:
            self.restart_window()

    def restart_window(self):
        """
        This function creates a new game window after choosing to restart.
        :return: None.
        """
        self._cover_frame = tki.Frame(self._buttons_frame, bg='gray', width=200, height=200)
        self._cover_frame.grid(row=0, column=0, rowspan=len(self._letters_board),
                               columnspan=len(self._letters_board[0]),
                               sticky='nsew')
        self._cover_frame.lift()
        restart_root = tki.Toplevel()
        restart_root.resizable(False, False)
        restart_root.title("BOGGLE - GAME OVER")
        self._toplevel = restart_root
        restart_button = tki.Button(self._toplevel, text="RESTART", font=('Helvetica', 30), borderwidth=3,
                                    relief=tki.RAISED, bg='orange', activebackground='dark orange', width='6',
                                    command=self.restart_game)
        restart_button.grid(row=0, column=0, sticky="nsew")
        photo = tki.PhotoImage(file="end_game.gif")

        frameCnt = 15
        frames = [tki.PhotoImage(file='end_game.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            self._toplevel_after1 = self._toplevel.after(100, update, ind)

        label = tki.Label(restart_root, image=photo, width=380, height=300)
        label.grid(row=1, column=0)
        exit_button = tki.Button(self._toplevel, text="QUIT GAME", font=('Helvetica', 30), borderwidth=3,
                                 relief=tki.RAISED, bg='orange', activebackground='dark orange', width='6',
                                 command=exit)
        exit_button.grid(row=2, column=0, sticky="nsew")
        self._toplevel_after2 = self._toplevel.after(0, update, 0)

    def _button_pressed(self, event: Any) -> None:
        """
        This function changes the text on a pressed button.
        :return: None.
        """
        self._display_line['text'] = self._text

    def _clear_display(self):
        """
        This function deletes the pressed buttons, by order of press history.
        :return: None.
        """
        if len(self._pressed_buttons) > 0:
            coor = self._pressed_buttons.pop()
            chars_to_delete = len(self._chars_buttons[coor]['text'])
            self._text = self._text[:-chars_to_delete]
            self._display_line['text'] = self._text
            # if len(self._pressed_buttons) > 0:
            #     coor = self._pressed_buttons.pop()
            self._chars_buttons[coor]['background'] = BUTTON_REGULAR_COLOR
            self._chars_buttons[coor]['activebackground'] = BUTTON_ACTIVE_COLOR

    def set_menu_labels(self, word: str, score: int, word_score: int):
        """
        This function creates the labels of the menu and updates the player's score.
        :param word: The current found word.
        :param score: Current score of the player.
        :param word_score: The score of the found word.
        :return: None
        """
        if word not in self._score_dict:
            self._score_dict[word] = word_score
        else:
            if self._score_dict[word] < word_score:
                self._score_dict[word] = word_score

        str_display = ""
        for word, word_score in self._score_dict.items():
            str_display += word + ": " + str(word_score) + '\n'

        self._score_label['text'] = 'Score: ' + str(score)
        self._text_label['state'] = tki.NORMAL
        self._text_label.delete("1.0", "end")
        self._text_label.insert("end", str_display)
        self._text_label['state'] = tki.DISABLED

        for coor in self._pressed_buttons:
            if self._dark_status == 0:
                self._chars_buttons[coor]['bg'] = REGULAR_BUTTON_REGULAR_COLOR
            else:
                self._chars_buttons[coor]['bg'] = DARK_BUTTON_REGULAR_COLOR
        self._pressed_buttons = []
        self._text = ""
        self._display_line['text'] = self._text

    def _dark_mode(self):
        """
        This function switch the colors theme of the game after clicking the checkbox button.
        :return: None.
        """
        global BUTTON_REGULAR_COLOR, BUTTON_ACTIVE_COLOR, BUTTON_PRESS_COLOR, MANAGE_BUTTON_COLOR, FRAME_COLOR, OUTER_FRAME_COLOR

        if self._dark_status == 0:
            BUTTON_REGULAR_COLOR = DARK_BUTTON_REGULAR_COLOR
            BUTTON_ACTIVE_COLOR = DARK_BUTTON_ACTIVE_COLOR
            BUTTON_PRESS_COLOR = DARK_BUTTON_PRESS_COLOR
            MANAGE_BUTTON_COLOR = DARK_MANAGE_BUTTON_COLOR
            FRAME_COLOR = DARK_FRAME_COLOR
            OUTER_FRAME_COLOR = DARK_OUTER_FRAME_COLOR
            self._clock_label['bg'] = DARK_FRAME_COLOR
            self._clock_label['fg'] = DARK_FRAME_FOREGROUND
            self._score_label['bg'] = DARK_FRAME_COLOR
            self._score_label['fg'] = DARK_FRAME_FOREGROUND
            self._display_line['bg'] = DARK_FRAME_COLOR
            self._display_line['fg'] = DARK_FRAME_FOREGROUND
            self._outer_frame['bg'] = DARK_FRAME_COLOR
            self._outer_frame['highlightbackground'] = DARK_FRAME_COLOR
            self._center_frame['bg'] = DARK_FRAME_COLOR
            self._bottom_frame['bg'] = DARK_FRAME_COLOR
            self._top_frame['bg'] = DARK_FRAME_COLOR
            self._top_frame['highlightbackground'] = DARK_FRAME_COLOR
            self._buttons_frame['bg'] = DARK_FRAME_COLOR
            self._text_label['bg'] = DARK_FRAME_COLOR
            self._text_label['fg'] = DARK_FRAME_FOREGROUND
            self._right_frame['bg'] = DARK_FRAME_COLOR
            for button in self._chars_buttons.values():
                if button['bg'] == REGULAR_BUTTON_PRESS_COLOR:
                    button['bg'] = DARK_BUTTON_PRESS_COLOR
                else:
                    button['bg'] = DARK_BUTTON_REGULAR_COLOR
                button['fg'] = DARK_FRAME_FOREGROUND
            self._dark_status = 1

        else:
            self._clock_label['bg'] = REGULAR_FRAME_COLOR
            self._clock_label['fg'] = REGULAR_FRAME_FOREGROUND
            self._score_label['bg'] = REGULAR_FRAME_COLOR
            self._score_label['fg'] = REGULAR_FRAME_FOREGROUND
            self._display_line['bg'] = REGULAR_FRAME_COLOR
            self._display_line['fg'] = REGULAR_FRAME_FOREGROUND
            self._outer_frame['bg'] = REGULAR_FRAME_COLOR
            self._outer_frame['highlightbackground'] = REGULAR_FRAME_COLOR
            self._center_frame['bg'] = REGULAR_FRAME_COLOR
            self._bottom_frame['bg'] = REGULAR_FRAME_COLOR
            self._top_frame['bg'] = REGULAR_FRAME_COLOR
            self._top_frame['highlightbackground'] = REGULAR_FRAME_COLOR
            self._buttons_frame['bg'] = REGULAR_FRAME_COLOR
            self._text_label['bg'] = REGULAR_FRAME_COLOR
            self._text_label['fg'] = REGULAR_FRAME_FOREGROUND
            self._right_frame['bg'] = REGULAR_FRAME_COLOR

            for button in self._chars_buttons.values():
                if button['bg'] == DARK_BUTTON_PRESS_COLOR:
                    button['bg'] = REGULAR_BUTTON_PRESS_COLOR
                else:
                    button['bg'] = REGULAR_BUTTON_REGULAR_COLOR
                button['fg'] = REGULAR_FRAME_FOREGROUND
            BUTTON_REGULAR_COLOR = REGULAR_BUTTON_REGULAR_COLOR
            BUTTON_ACTIVE_COLOR = REGULAR_BUTTON_ACTIVE_COLOR
            BUTTON_PRESS_COLOR = REGULAR_BUTTON_PRESS_COLOR
            MANAGE_BUTTON_COLOR = REGULAR_MANAGE_BUTTON_COLOR
            FRAME_COLOR = REGULAR_FRAME_COLOR
            OUTER_FRAME_COLOR = REGULAR_OUTER_FRAME_COLOR
            self._dark_status = 0

    def get_text(self):
        """
        A getter function of the game's current text that is displayed.
        :return: Current text that is displayed.
        """
        return self._text

    def get_curr_path(self):
        """
        A getter function of the game's current path.
        :return: Current path.
        """
        return self._pressed_buttons

    def restart_game(self):
        """
        This function start a new Boggle game.
        :return: None.
        """
        if self._dark_status == 1:
            self._dark_mode()
        for after_id in self._toplevel.tk.eval('after info').split():
            self._toplevel.after_cancel(after_id)
        for after_id in self._main_window.tk.eval('after info').split():
            self._main_window.after_cancel(after_id)
        self._toplevel.destroy()
        self._main_window.destroy()
        self._restart = True


if __name__ == "__main__":
    pass
