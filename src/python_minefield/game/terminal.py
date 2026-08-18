# game/terminal.py

import shutil
import sys
import termios
import tty

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

MIN_CELL_SIZE = 1


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


def normalize_cell_size(cell_size: int | None) -> int:
    """Normalizes the cell size ensuring it is an odd number for symmetrical rendering.

    Args:
        cell_size: The target cell width or height (must be an integer > 0).

    Returns:
        int: The original size if odd, or cell_size + 1 if even.

    Raises:
        TypeError: If cell_size is not an integer (e.g., float, str, None, bool).
        ValueError: If cell_size is an integer <= 0.
    """
    if not isinstance(cell_size, int) or isinstance(cell_size, bool):
        raise TypeError(
            f"cell_size must be an integer (int), got: {type(cell_size).__name__}"
        )

    if cell_size <= 0:
        raise ValueError(
            f"cell_size must be a positive integer (> 0), got: {cell_size}"
        )

    if cell_size % 2 == 0:
        return cell_size + 1

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
