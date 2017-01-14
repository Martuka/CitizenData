#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is currently just a draft of the UI, to see how curses library functions.
import curses
from curses import wrapper

words = {'papa': [0.003, 0.321], 'mama': [0.004, 0.555], 'utilisation': [0.345, 0.020], 'pesticide': [0.123, 0.513], 'synthèse': [0.987, 0.040], 'production': [0.738, 0.052], 'transformation': [0.014, 0.042], 'produit': [0.988, 0.006], 'territoire': [0.123, 0.312], 'importation': [0.654, 0.009], 'commercial': [0.824, 0.888], 'denrée': [0.936, 0.222], 'pesticide': [0.234, 0.777], 'synthèse': [0.999, 0.007], 'production': [0.321, 0.492], 'pesticide': [0.294, 0.811], 'synthèse': [0.002, 0.391], 'confédération': [0.003, 0.007], 'conséquence': [0.001, 0.515], 'cartel': [0.901, 0.081]}
title = "Pour une Suisse libre de pesticides de synthèse"
content = "L’utilisation de tout pesticide de synthèse dans la production agricole, la transformation des produits agricoles et l’entretien du territoire est interdite. L’importation à des fins commerciales de denrées alimentaires contenant des pesticides de synthèse ou pour la production desquelles des pesticides de synthèse ont été utilisés est interdite."
date = "2009"
opinions = {"Pour": [0.123, 0.987], "Contre": [0.913, 0.666]}

# setting up curses terminal window
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.immedok(True)

stdscr.border(1)
stdscr.addstr(3, 3, "Screensize is {} by {}".format(curses.LINES, curses.COLS))

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
begin_x = 20; begin_y = 7
height = 5; width = 40
win = curses.newwin(height, width, begin_y, begin_x)
win.bkgd(curses.COLOR_RED)
win.box()
s = "Current mode: Typing mode"
win.addstr(height//2, width//2 - len(s)//2, s, curses.A_REVERSE)
win.noutrefresh()
curses.doupdate()
# stdscr.refresh()

while True:
	event = stdscr.getch()
	if event == ord("q"): break
# unsetting to restore terminal tu usual behavior
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()


# def main(stdscr):
#     # Clear screen
#     stdscr.clear()
#
#     # This raises ZeroDivisionError when i == 10.
#     for i in range(0, 11):
#         v = i-10
#         stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))
#
#     stdscr.refresh()
#     stdscr.getkey()
#
# wrapper(main)
