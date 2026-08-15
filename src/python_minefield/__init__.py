import random

from .game.terminal import clear_screen, hide_cursor, show_cursor
from .game.core import select_difficulty, check_victory, count_adjacent_mines, flood_fill, get_key
from .game.math import random_int, get_adjacent_indices
from .game.config import COVERED, DIFFICULTIES, FLAG, MINE, NUM_COLORS, SPACE
from .game.colors import GRAY, GREEN, RED, RESET
from .game.board import display_board

def main():
    clear_screen()
    message = ""
    cursor_idx = 0

    cell_w = 3
    cell_h = 1

    real_board = []
    visible_board = []

    chosen_difficulty = select_difficulty()
    clear_screen()

    config = DIFFICULTIES[chosen_difficulty]

    board_cols = config["cols"]
    board_rows = config["rows"]
    board_size = board_cols * board_rows

    percentage = config["percent"]

    mines_cnt = max(1, round(board_size * percentage))        

    for i in range(board_cols):
        for _ in range(board_rows):
            real_board.append(SPACE)
            visible_board.append(COVERED)

    start_point = random_int(0, board_size - 1)
    forbidden_points = get_adjacent_indices(start_point, board_rows, board_cols)
    forbidden_points.append(start_point) 

    allowed_indices = [i for i in range(board_size) if i not in forbidden_points]

    mine_indices = random.sample(allowed_indices, mines_cnt)
    for idx in mine_indices:
        real_board[idx] = MINE


    for i, cell in enumerate(real_board):
        if cell == MINE:
            continue

        mines = count_adjacent_mines(i, real_board, board_rows, board_cols)

        if mines > 0:
            color = NUM_COLORS[mines]
            real_board[i] = f"{color}{mines}{RESET}"
        else:
            real_board[i] = SPACE

    flood_fill(start_point, real_board, visible_board, board_rows, board_cols) 

    while True:
        display_board(visible_board, board_cols, board_rows, cell_w, cell_h, cursor_idx)

        key = get_key()

        r = cursor_idx // board_cols
        c = cursor_idx % board_cols

        if key == "UP" and r > 0:
            cursor_idx -= board_cols
        elif key == "DOWN" and r < board_rows - 1:
            cursor_idx += board_cols
        elif key == "LEFT" and c > 0:
            cursor_idx -= 1
        elif key == "RIGHT" and c < board_cols - 1:
            cursor_idx += 1

        elif key == "FLAG":
            if visible_board[cursor_idx] == COVERED:
                visible_board[cursor_idx] = FLAG
            else:
                visible_board[cursor_idx] = COVERED

        elif key == "ENTER":
            visible_board[cursor_idx] = real_board[cursor_idx]

            if real_board[cursor_idx] == MINE:
                message = f"{RED}Ahhhhhhhhhhhhhhh{RESET}"
                break
            elif real_board[cursor_idx] != SPACE:
                visible_board[cursor_idx] = real_board[cursor_idx]
            else:
                flood_fill(cursor_idx, real_board, visible_board, board_rows, board_cols)

            if (check_victory(real_board, visible_board)):
                message = f"{GREEN}Victory is yours!!!{RESET}"
                break

        elif key == "ESC":
            message = f"{GRAY}Exiting...{RESET}"
            break

    display_board(real_board, board_cols, board_rows, cell_w, cell_h, cursor_idx)

    if message:
        print(f"\n{message}")

if __name__ == "__main__":
    hide_cursor()

    try:
        main()
    finally:
        show_cursor()