#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is currently just a draft of the UI,
# to see how curses library functions.
import sys
import signal
import curses
import math
import random


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
    for i in range(5, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    ################################
    # Initiative text display window
    win_text_y_pos = 0
    win_text_x_pos = 0
    win_text_height = math.floor(2*screen_dims[0]/3)
    win_text_width = math.floor(3*screen_dims[1]/4)
    win_text = curses.newwin(win_text_height, win_text_width, win_text_y_pos, win_text_x_pos)
    win_text.attrset(curses.color_pair(5))
    win_text.border(0, 0, 0, 1, 0, 0, 0, 0)
    win_text.noutrefresh()

    global inner_text_win
    inner_text_win = curses.newwin(win_text_height-4, win_text_width-8, win_text_y_pos+2, win_text_x_pos+4)
    inner_text_win.attrset(win_text.getbkgd())
    inner_text_win.scrollok(True)
    inner_text_win.idlok(0)
    # inner_text_win.noutrefresh()
    # curses.doupdate()

    ###################################
    # Nouns frequencies and predictions window
    win_nouns_y_pos = win_text_height - 1
    win_nouns_x_pos = 0
    win_nouns_height = screen_dims[0] - win_text_height + 1
    win_nouns_width = win_text_width
    global win_nouns
    win_nouns = curses.newwin(win_nouns_height, win_nouns_width, win_nouns_y_pos, win_nouns_x_pos)
    win_nouns.attrset(curses.color_pair(5))
    win_nouns.clear()
    win_nouns.border(0, 0, 1, 0, curses.ACS_VLINE, curses.ACS_VLINE, 0, 0)
    win_nouns.noutrefresh()

    global inner_nouns_win
    inner_nouns_win = curses.newwin(win_nouns_height-2, win_nouns_width-4, win_nouns_y_pos+1, win_nouns_x_pos+2)
    # inner_nouns_win.noutrefresh()


    #############################
    # Date window
    win_date_y_pos = 0
    win_date_x_pos = win_text_width
    global win_date_height
    win_date_height = screen_dims[0]//3 + 2
    global win_date_width
    win_date_width = screen_dims[1] - win_text_width
    global win_date
    win_date = curses.newwin(win_date_height, win_date_width, win_date_y_pos, win_date_x_pos)
    win_date.attrset(curses.color_pair(5))
    # win_date.border(0, 1, 1, 0, 1, 1, 1, 1)
    # win_date.noutrefresh()

    ######################
    # Opinion window
    win_op_y_pos = win_date_height - 1
    win_op_x_pos = win_date_x_pos
    win_op_height = win_date_height
    win_op_width = win_date_width
    global win_op
    win_op = curses.newwin(win_op_height, win_op_width, win_op_y_pos, win_op_x_pos)
    win_op.attrset(curses.color_pair(5))
    # win_op.border(0, 1, 1, 1, 1, 1, 1, 1)
    s = "Pour and Contre"
    win_op.addstr(win_op_height//2, win_op_width//2 - len(s)//2, s, curses.color_pair(3))
    # win_op.noutrefresh()

    ##############################
    # Verbs and adjectives window
    win_adj_y_pos = win_nouns_y_pos
    win_adj_x_pos = win_date_x_pos
    win_adj_height = win_nouns_height
    win_adj_width = win_date_width
    global win_adj
    win_adj = curses.newwin(win_adj_height, win_adj_width, win_adj_y_pos, win_adj_x_pos)
    win_adj.attrset(curses.color_pair(5))
    # win_adj.border(0, 1, 1, 1, 1, 1, 1, 1)
    s = "Verbs and adjectives"
    win_adj.addstr(win_adj_height//2, win_adj_width//2 - len(s)//2, s, curses.color_pair(3))
    # win_adj.noutrefresh()

    curses.doupdate()

    # Register signal handlers for graceful exit on for instance CTRL-C
    signal.signal(signal.SIGINT, prepare_exit_and_quit)
    signal.signal(signal.SIGTERM, prepare_exit_and_quit)


glyph = {
    '0': [" ##### ",
          " #   # ",
          " #   # ",
          " #   # ",
          " #   # ",
          " #   # ",
          " ##### "],

    '1': ["   # ",
          "   # ",
          "   # ",
          "   # ",
          "   # ",
          "   # ",
          "   # "],

    '2': [" ##### ",
          "     # ",
          "     # ",
          " ##### ",
          " #     ",
          " #     ",
          " ##### "],

    '3': [" ##### ",
          "     # ",
          "     # ",
          " ##### ",
          "     # ",
          "     # ",
          " ##### "],

    '4': [" #   # ",
          " #   # ",
          " #   # ",
          " ##### ",
          "     # ",
          "     # ",
          "     # "],

    '5': [" ##### ",
          " #     ",
          " #     ",
          " ##### ",
          "     # ",
          "     # ",
          " ##### "],

    '6': [" ##### ",
          " #     ",
          " #     ",
          " ##### ",
          " #   # ",
          " #   # ",
          " ##### "],

    '7': [" ##### ",
          "     # ",
          "     # ",
          "     # ",
          "     # ",
          "     # ",
          "     # "],

    '8': [" ##### ",
          " #   # ",
          " #   # ",
          " ##### ",
          " #   # ",
          " #   # ",
          " ##### "],

    '9': [" ##### ",
          " #   # ",
          " #   # ",
          " ##### ",
          "     # ",
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
    disp_array = ["" for i in range(0, 7)]
    one = True if now[0] == '1' else False
    for char in year:
        char_array = glyph[char]
        for row in range(0, len(char_array)):
            disp_array[row] += char_array[row]
    window.clear()
    for y in range(0, len(disp_array)):
        for x in range(0, len(disp_array[y])):
            a = x-1 if now[0] == '1' else x
            char = disp_array[y][x]
            color = curses.A_REVERSE if char == " " else 4
            addstr(window, y, a, " ", curses.color_pair(color), len(disp_array), len(disp_array[y]))
    window.noutrefresh()
    curses.doupdate()


def display_year(window, string):
    # getcolor(color)
    now = string
    print_year(window, now)


# def print_srt(win, y, x, string, title):
#     if title:
#         win.clear()
#     win.addstr(y, x, string, win.getbkgd())
#     if not title:
#         win.noutrefresh()
#         curses.doupdate()

def print_srt(win, y, x, string, string2):
    win.clear()
    win.addstr(y, x, string, win.getbkgd())
    win.addstr(y + 2, x, string2, win.getbkgd())
    win.noutrefresh()
    curses.doupdate()


def print_str(win, y, x, string, color, s_height, s_len):
    win.addstr(y, x, string, color)


def print_noun_values(win, lst):
    """will display the nouns list in
    4 cols and 10 lines grid
    """
    mx, idx = max((lst[idx][1][1], idx) for idx in range(len(lst)))
    idx += 1
    h, w = win.getmaxyx()
    pos_y = (h - 10)//2
    len_x = w//4
    val_space = 15
    tab = 4
    color = win.getbkgd()
    pred_tab = len_x - val_space
    win.clear()
    list_len = len(lst)
    i = 0
    try:
        for y in range(0, 5):
            for x in range(0, 4):
                i += 1
                if i > list_len:
                    raise StopIteration
                word = lst[i-1][0]
                real = "{0:.6f}".format(lst[i-1][1][0])
                space = len_x - tab - val_space - len(word)
                win.addstr(pos_y + 2*y, x * len_x + tab, word + space*" " + " [  ", color)
                win.addstr(pos_y + 2*y, x * len_x + tab + len(word) + space + 4, real + "%", curses.color_pair(9))
                win.addstr(pos_y + 2*y, x * len_x + tab + len(word) + space + 13, "]", color)

                pred = "{0:.6f}".format(lst[i-1][1][1])
                win.addstr(pos_y + 2*y + 1, x*len_x + pred_tab, " [  " + pred + "%]", color)
                if not random.randrange(0, 6): # to keep for later use if i == idx:
                    win.addstr(pos_y + 2*y + 1, x*len_x + pred_tab + 4, pred + "%", curses.A_REVERSE)
                else:
                    win.addstr(pos_y + 2*y + 1, x*len_x + pred_tab + 4, pred + "%", curses.color_pair(6))
                win.addstr(pos_y + 2*y + 1, x*len_x + pred_tab + 13, "]", color)
    except StopIteration:
        pass
    win.noutrefresh()
    curses.doupdate()


def print_opinion_window(win, lst1, lst2):
    h, w = win.getmaxyx()
    len_x = 2*w//3
    pos_y = (h - 4)//2 - 2
    color = win.getbkgd()
    val_space = 15
    tab = w//6
    for_len = len("pour")
    ag_len = len("contre")
    space_for = len_x - for_len - val_space
    space_ag = len_x - ag_len - val_space
    win.clear()

    # redraw the border
    for i in range(0, w):
        win.addch(0, i, curses.ACS_HLINE)

    win.addstr(pos_y, tab + 2, lst1[0] + space_for*" " + "[  ", color)
    win.addstr(pos_y, tab + 2 + for_len + space_for + 3, "{0:.6f}".format(lst1[1][0]) + "%", curses.color_pair(9))
    win.addstr(pos_y, tab + 2 + for_len + space_for + 3 + 9, "]", color)

    win.addstr(pos_y+1, tab + 2 + len_x - val_space, "[  ", color)
    win.addstr(pos_y+1, tab + 2 + len_x - val_space + 3, "{0:.6f}".format(lst1[1][1]) + "%", curses.color_pair(6))
    win.addstr(pos_y+1, tab + 2 + len_x - val_space + 3 + 9, "]", color)

    win.addstr(pos_y+3, tab + 2, lst2[0] + space_ag*" " + "[  ", color)
    win.addstr(pos_y+3, tab + 2 + ag_len + space_ag + 3, "{0:.6f}".format(lst2[1][0]) + "%", curses.color_pair(9))
    win.addstr(pos_y+3, tab + 2 + ag_len + space_ag + 3 + 9, "]", color)

    win.addstr(pos_y+4, tab + 2 + len_x - val_space, "[  ", color)
    win.addstr(pos_y+4, tab + 2 + len_x - val_space + 3, "{0:.6f}".format(lst2[1][1]) + "%", curses.color_pair(6))
    win.addstr(pos_y+4, tab + 2 + len_x - val_space + 3 + 9, "]", color)

    win.noutrefresh()
    curses.doupdate()


def print_verb_adj_window(win, lverbs, ladjs):
    h, w = win.getmaxyx()
    len_x = w//2
    pos_y = (h - 5)//2
    color = win.getbkgd()
    tab = len_x//4
    win.clear()
    for i in range(0, w):
        win.addch(0, i, curses.ACS_HLINE)
    for i in range(0, 5):
        if i < len(lverbs):
            win.addstr(pos_y+i, tab, lverbs[i][0], color)
        if i < len(ladjs):
            win.addstr(pos_y+i, len_x+tab, ladjs[i][0], color)
    win.noutrefresh()
    curses.doupdate()


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
