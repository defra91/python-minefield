# game/terminal.py

import sys
import shutil
import termios
import tty

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def hide_cursor():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()

def clear_screen():
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

def get_terminal_width():
    """Returns the current terminal width in columns (default 80)."""
    return shutil.get_terminal_size((80, 20)).columns

def normalize_cell_size(cell_size):
    if (cell_size % 2 == 0):
        return cell_size + 1
    else:
        return cell_size

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            if ch2 == "[":
                return {
                    "A": "UP",
                    "B": "DOWN",
                    "D": "LEFT",
                    "C": "RIGHT",
                }.get(ch3)
            return "ESC"
        elif ch in ("\r", "\n"):
            return "ENTER"
        elif ch == " ":
            return "SPACE"
        elif ch.lower() == "f":
            return "FLAG"
        elif ch.lower() == "q":
            return "ESC"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None