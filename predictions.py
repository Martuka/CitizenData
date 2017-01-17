#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import signal
import time
import curses
from curses import wrapper
import config
import math
import random
import utils


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
    screen.immedok(True)    # supposed to refresh the view automatically

    screen.border(1)
    screen_dims = screen.getmaxyx()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    for i in range(5, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    ################################
    # Generated text display window
    w_t_y_pos = 0
    w_t_x_pos = 0
    w_t_height = screen_dims[0]
    w_t_width = math.floor(3*screen_dims[1]/4)
    win_text = curses.newwin(w_t_height, w_t_width, w_t_y_pos, w_t_x_pos)
    win_text.attrset(curses.color_pair(5))
    win_text.border(0, 0, 0, 0, 0, 0, 0, 0)
    win_text.noutrefresh()

    global inner_text_win
    inner_text_win = curses.newwin(w_t_height-4, w_t_width-8, w_t_y_pos+2, w_t_x_pos+4)
    inner_text_win.attrset(win_text.getbkgd())
    inner_text_win.scrollok(True)
    inner_text_win.idlok(0)
    # inner_text_win.noutrefresh()
    # curses.doupdate()

    ###################################
    # Nouns frequencies and predictions window
    win_nouns_y_pos = w_t_height - 1
    win_nouns_x_pos = 0
    win_nouns_height = screen_dims[0] - w_t_height + 1
    win_nouns_width = w_t_width


    #############################
    # Date window
    win_date_y_pos = 0
    win_date_x_pos = w_t_width
    global win_date_height
    win_date_height = screen_dims[0]//3 + 2
    global win_date_width
    win_date_width = screen_dims[1] - w_t_width
    global win_date
    win_date = curses.newwin(win_date_height, win_date_width, win_date_y_pos, win_date_x_pos)
    win_date.attrset(curses.color_pair(5))
    # win_date.border(0, 1, 1, 0, 1, 1, 1, 1)
    # win_date.noutrefresh()

    ######################
    # Opinion window
    win_op_y_pos = win_date_height - 1
    win_op_x_pos = win_date_x_pos
    win_op_height = screen_dims[0] - win_date_height + 1
    win_op_width = win_date_width
    global win_op
    win_op = curses.newwin(win_op_height, win_op_width, win_op_y_pos, win_op_x_pos)
    win_op.attrset(curses.color_pair(5))
    # win_op.border(1, 1, 0, 1, 1, 1, 1, 1)
    # win_op.noutrefresh()


    curses.doupdate()

    # Register signal handlers for graceful exit on for instance CTRL-C
    signal.signal(signal.SIGINT, prepare_exit)
    signal.signal(signal.SIGTERM, prepare_exit)


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
        char_array = config.glyph[char]
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
    now = string
    print_year(window, now)


def print_s(win, y, x, string, first, last):
    if first:
        win.clear()

    win.addstr(y, x, string, win.getbkgd())
    if last:
        win.noutrefresh()
        curses.doupdate()


def print_generated_texts(win, lst_titles):
    h, w = win.getmaxyx()
    nb = len(lst_titles)
    y_pos = h//(nb+1)
    for i in range(0, nb):
        first = True if (i == 0) else False
        last = True if (i == nb-1) else False
        print_s(win, y_pos*(i+1), 5, lst_titles[i], first, last)


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


def draw_window_border(win):
    h, w = win.getmaxyx()
    win.clear()
    # redraw the border
    for i in range(0, w):
        win.addch(0, i, curses.ACS_HLINE)
        # win.addch(h, i, curses.ACS_HLINE)
    win.noutrefresh()
    curses.doupdate()

def draw_window_adj_border(win):
    h, w = win.getmaxyx()
    win.clear()
    # redraw the border
    for i in range(0, w):
        win.addch(0, i, curses.ACS_HLINE)
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


def random_x_list(n, l):
    i = 0
    res = []
    while i < n:
        k = random.randrange(0, l)
        if k not in res:
            res.append(k)
            i += 1
    return res


def prepare_exit(signal, frame):
    pretty_quit("")


def pretty_quit(err):
    # unsetting to restore terminal to usual behavior
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)
    curses.endwin()
    if not err == "":
        print(err)
    sys.exit(0)


def log(t, s):
    with open("logs.txt", "a") as log_file:
        print('{} :: {}'.format(t, s), file=log_file)


def main():
    try:
        init()
        counter = 2017
        NUMBER_OF_TEXTS = 5
        while True:
            display_year(win_date, str(counter))
            draw_window_border(win_op)
            # draw_window_adj_border(win_adj)
            titles_list = []
            texts = utils.list_the_file("generation.txt")
            indexes = random_x_list(NUMBER_OF_TEXTS, len(texts))
            for v in indexes:
                titles_list.append(texts[v])
            print_generated_texts(inner_text_win, titles_list)
            counter += 1
            time.sleep(5)
            # screen.getkey()
    except Exception as err:
        t = sys.exc_info()[0].__name__
        f = str(os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename))
        l = str(sys.exc_info()[2].tb_lineno)
        # details = "{}: {} in file: {} at line: {}".format(t, err, f, l)
        details = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(err), err
        pretty_quit(details)


if __name__ == "__main__":
    main()
