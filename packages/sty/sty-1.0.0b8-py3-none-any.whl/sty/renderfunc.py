"""
A selection of render functions.

These functions generate the escape-sequences that trigger certain
colors/effects in the terminals.
"""


def sgr(num):
    return '\033[' + str(num) + 'm'


def eightbit_fg(num):
    return '\033[38;5;' + str(num) + 'm'


def eightbit_bg(num):
    return '\033[48;5;' + str(num) + 'm'


def rgb_fg(r, g, b):
    return '\x1b[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'


def rgb_bg(r, g, b):
    return '\x1b[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
