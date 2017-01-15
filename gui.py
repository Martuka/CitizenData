#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is currently just a draft of the UI,
# to see how curses library functions.
import curses
from curses import wrapper
import math
import signal
import sys


def init():
    # setting up curses terminal window
    global screen
    screen = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    screen.keypad(True)
    screen.immedok(True) # supposed to refresh the view automatically

    screen.border(1)
    # screen.addstr(3, 3, "Screensize is {} by {}".format(curses.LINES, curses.COLS))
    screen_dims = screen.getmaxyx()
    # screen.addstr(4, 3, "Or is it {} by {}?".format(screen_dims[0], screen_dims[1]))


    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Initiative text display window
    win_text_y_pos = 0
    win_text_x_pos = 0
    win_text_height = math.floor(2*screen_dims[0]/3)
    win_text_width = math.floor(3*screen_dims[1]/4)
    global win_text
    win_text = curses.newwin(win_text_height, win_text_width, win_text_y_pos, win_text_x_pos)
    win_text.attrset(curses.color_pair(8))

    # windows with frame without botton line and bottom left and right corners
    # windows.border(args)
    # args: left, top, right, bottom,
    # t-l-corner, t-r-corner, b-l-corner, b-r-corner
    win_text.border(0, 0, 0, 1, 0, 0, 0, 0)
    s = "Initiative Content"
    win_text.addstr(win_text_height//2, win_text_width//2 - len(s)//2, s, curses.color_pair(3))
    win_text.noutrefresh()

    global inner_text_win
    inner_text_win = curses.newwin(win_text_height-4, win_text_width-4, win_text_y_pos+2, win_text_x_pos+2)
    inner_text_win.noutrefresh()
    # curses.doupdate()

    # Nouns frequencies and predictions window
    win_nouns_y_pos = win_text_height - 1
    win_nouns_x_pos = 0
    win_nouns_height = screen_dims[0] - win_text_height + 1
    win_nouns_width = win_text_width
    global win_nouns
    win_nouns = curses.newwin(win_nouns_height, win_nouns_width, win_nouns_y_pos, win_nouns_x_pos)
    win_nouns.attrset(curses.color_pair(8))
    win_nouns.clear()
    win_nouns.border(0, 0, 1, 0, 0, 0, 0, 0)
    s = "Nouns Frequencies"
    win_nouns.addstr(win_nouns_height//2, win_nouns_width//2 - len(s)//2, s, curses.A_REVERSE)
    win_nouns.noutrefresh()


    # Date window
    win_date_y_pos = 0
    win_date_x_pos = win_text_width
    global win_date_height
    win_date_height = screen_dims[0]//3 + 2
    global win_date_width
    win_date_width = screen_dims[1] - win_text_width
    global win_date
    win_date = curses.newwin(win_date_height, win_date_width, win_date_y_pos, win_date_x_pos)
    win_date.attrset(curses.color_pair(8))
    win_date.border(0, 1, 1, 0, 1, 1, 1, 1)
    display_year(win_date, "2010", "cyan")
    win_date.noutrefresh()

    # Opinion window
    win_op_y_pos = win_date_height - 1
    win_op_x_pos = win_date_x_pos
    win_op_height = win_date_height
    win_op_width = win_date_width
    global win_op
    win_op = curses.newwin(win_op_height, win_op_width, win_op_y_pos, win_op_x_pos)
    win_op.attrset(curses.color_pair(8))
    win_op.border(0, 1, 1, 1, 1, 1, 1, 1)
    s = "Pour and Contre"
    win_op.addstr(win_op_height//2, win_op_width//2 - len(s)//2, s, curses.color_pair(3))
    win_op.noutrefresh()

    # Verbs and adjectives window
    win_adj_y_pos = win_nouns_y_pos
    win_adj_x_pos = win_date_x_pos
    win_adj_height = win_nouns_height
    win_adj_width = win_date_width
    global win_adj
    win_adj = curses.newwin(win_adj_height, win_adj_width, win_adj_y_pos, win_adj_x_pos)
    win_adj.attrset(curses.color_pair(8))
    win_adj.border(0, 1, 1, 1, 1, 1, 1, 1)
    s = "Verbs and adjectives"
    win_adj.addstr(win_adj_height//2, win_adj_width//2 - len(s)//2, s, curses.color_pair(3))
    win_adj.noutrefresh()

    curses.doupdate()

    # Register signal handlers for graceful exit on for instance CTRL-C
    signal.signal(signal.SIGINT, prepare_exit_and_quit)
    signal.signal(signal.SIGTERM, prepare_exit_and_quit)


glyph = {
    '0': [" ##### ",
          " #   # ",
          " #   # ",
          " #   # ",
          " ##### "],

    '1': ["   # ",
          "   # ",
          "   # ",
          "   # ",
          "   # "],

    '2': [" ##### ",
          "     # ",
          " ##### ",
          " #     ",
          " ##### "],

    '3': [" ##### ",
          "     # ",
          " ##### ",
          "     # ",
          " ##### "],

    '4': [" #   # ",
          " #   # ",
          " ##### ",
          "     # ",
          "     # "],

    '5': [" ##### ",
          " #     ",
          " ##### ",
          "     # ",
          " ##### "],

    '6': [" ##### ",
          " #     ",
          " ##### ",
          " #   # ",
          " ##### "],

    '7': [" ##### ",
          "     # ",
          "     # ",
          "     # ",
          "     # "],

    '8': [" ##### ",
          " #   # ",
          " ##### ",
          " #   # ",
          " ##### "],

    '9': [" ##### ",
          " #   # ",
          " ##### ",
          "     # ",
          " ##### "]
}


def getcolor(color):
    colors = {
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
        "orange": 9,
    }

    curses.init_pair(6, 0, -1)
    curses.init_pair(7, colors[color], -1)
    curses.init_pair(8, 0, colors[color])


def addstr(window, y, x, string, color, char_height, char_width):
    window.addstr((win_date_height//2 - char_height//2)+y, (win_date_width//2 - char_width//2)+x, string, color)


def print_year(window, now):
    year = now
    disp_array = ["" for i in range(0, 5)]

    for char in year:
        char_array = glyph[char]
        for row in range(0, len(char_array)):
            disp_array[row] += char_array[row]
    window.clear()
    for y in range(0, len(disp_array)):
        for x in range(0, len(disp_array[y])):
            char = disp_array[y][x]
            color = curses.A_REVERSE if char == " " else 1
            addstr(window, y, x + 2, " ", curses.color_pair(color), len(disp_array), len(disp_array[y]))
    window.noutrefresh()
    curses.doupdate()


def display_year(window, string, color):
    getcolor(color)
    now = string
    print_year(window, now)


def print_srt(win, y, x, string):
    win.clear()
    win.addstr(y, x, string, win.getbkgd())
    win.noutrefresh()
    curses.doupdate()


def print_str(win, y, x, string, color, s_height, s_len):
    win.addstr(y, x, string, color)


def prepare_exit_and_quit(signal, frame):
    # unsetting to restore terminal to usual behavior
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)
    curses.endwin()
    sys.exit(0)


# def main(screen):
#     # Clear screen
#     screen.clear()
#
#     # This raises ZeroDivisionError when i == 10.
#     for i in range(0, 11):
#         v = i-10
#         screen.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))
#
#     screen.refresh()
#     screen.getkey()
#
# wrapper(main)
