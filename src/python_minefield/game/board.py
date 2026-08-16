# game/board.py

import sys

from . import terminal as terminal
from .colors import BLUE, BOLD, CURSOR_STYLE, GRAY, LIGHT_GRAY, RED, RESET
from .config import MINE, NUM_COLORS, SPACE
from .math import is_float

L_CORNER_TOP = f"{GRAY}╔{RESET}"
L_CORNER_BOTTOM = f"{GRAY}╚{RESET}"
BORDER_HORIZ = f"{GRAY}═{RESET}"
DIVIDER_TOP = f"{GRAY}╦{RESET}"
DIVIDER_BOTTOM = f"{GRAY}╩{RESET}"
R_CORNER_TOP = f"{GRAY}╗{RESET}"
R_CORNER_BOTTOM = f"{GRAY}╝{RESET}"
DIVIDER_MID = f"{GRAY}╬{RESET}"
L_DIVIDER_MID = f"{GRAY}╠{RESET}"
R_DIVIDER_MID = f"{GRAY}╣{RESET}"
BORDER_VERT = f"{GRAY}║{RESET}"


def board_row_top(cell_cnt, cell_size):
    row = L_CORNER_TOP

    cell_size = terminal.normalize_cell_size(cell_size)

    for i in range(cell_cnt):
        row += BORDER_HORIZ * cell_size

        if i < cell_cnt - 1:
            row += DIVIDER_TOP

    row += R_CORNER_TOP

    return row


def board_row_bottom(cell_cnt, cell_size):
    row = L_CORNER_BOTTOM

    cell_size = terminal.normalize_cell_size(cell_size)

    for i in range(cell_cnt):
        row += BORDER_HORIZ * cell_size

        if i < cell_cnt - 1:
            row += DIVIDER_BOTTOM

    row += R_CORNER_BOTTOM

    return row


def board_row_central(cell_cnt, cell_size, contents=[]):
    row = BORDER_VERT

    cell_size = terminal.normalize_cell_size(cell_size)

    for i in range(cell_cnt):
        for j in range(cell_size):
            if j == (cell_size - 1) / 2:
                c = contents[i]

                if c == "X":
                    c = f"{RED}{BOLD}X{RESET}"
                elif c == "O":
                    c = f"{BLUE}{BOLD}O{RESET}"
                else:
                    c = f"{LIGHT_GRAY}{c}{RESET}"

                row += c
            else:
                row += SPACE

        if i < cell_cnt - 1:
            row += BORDER_VERT

    row += BORDER_VERT

    return row


def board_row_central_divider_mid(cell_cnt, cell_size):
    row = L_DIVIDER_MID

    cell_size = terminal.normalize_cell_size(cell_size)

    for i in range(cell_cnt):
        row += BORDER_HORIZ * cell_size

        if i < cell_cnt - 1:
            row += DIVIDER_MID

    row += R_DIVIDER_MID

    return row


def display_board(board, cols, rows, cell_w, cell_h, cursor_idx):
    buffer = []

    buffer.append("\033[H")

    width = terminal.get_terminal_width()

    cell_w = terminal.normalize_cell_size(cell_w)
    cell_h = terminal.normalize_cell_size(cell_h)

    index = 0
    for i in range(rows):
        if i == 0:
            first_row = board_row_top(cols, cell_w)
        else:
            first_row = board_row_central_divider_mid(cols, cell_w)

        buffer.append(first_row.center(width + 18) + "\n")

        for j in range(cell_h):
            contents = [MINE] * cols

            if j == (cell_h - 1) / 2:
                for col_idx in range(cols):
                    c = board[index]
                    if c == "":
                        c = SPACE
                    if is_float(c):
                        c = int(c)
                        color = NUM_COLORS[int(c)]
                        c = f"{color}{c}{RESET}"

                    if index == cursor_idx:
                        contents[col_idx] = f"{CURSOR_STYLE}{c}{RESET}"
                    else:
                        contents[col_idx] = c

                    index += 1

            row = board_row_central(cols, cell_w, contents)
            buffer.append(row.center(width + 18) + "\n")

    bottom = board_row_bottom(cols, cell_w)
    buffer.append(bottom.center(width + 18) + "\n\n")

    sys.stdout.write("".join(buffer))
    sys.stdout.flush()
