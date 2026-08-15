import time

from .game.config import COVERED, DIFFICULTIES, FLAG, SPACE, MINE
from .game.core import (
    init_game,
    select_difficulty,
    check_victory,
    check_defeat,
    flood_fill,
    get_key,
    get_player_name,
    chording,
)
from .game.storage import save_game, load_game

from .game.terminal import clear_screen, hide_cursor, show_cursor
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

    player_name = get_player_name()
    game = load_game(player_name)
    current_game = game.get("current_game") if game else None
    stats = game.get("stats") if game else {"games_played": 0, "games_won": 0}

    if current_game:
        real_board = current_game["real_board"]
        visible_board = current_game["visible_board"]
        board_cols = current_game["cols"]
        board_rows = current_game["rows"]
        config = current_game
    else:
        chosen_difficulty = select_difficulty()
        clear_screen()
        config = DIFFICULTIES[chosen_difficulty]
        board_cols = config["cols"]
        board_rows = config["rows"]

        real_board, visible_board = init_game(config)

        save_game(
            player_name, 
            config["rows"], 
            config["cols"],
            real_board,
            visible_board,
            time.time())

    exit = False
    while not exit:
        display_board(visible_board, board_cols, board_rows, cell_w, cell_h, cursor_idx)

        print(f"{GRAY}Player: {player_name}{RESET}")
        print(f"{GRAY}Use arrow keys to move, Enter to reveal, F to flag, q to exit.{RESET}")
        print(f"{GRAY}Games played: {stats['games_played']}, Games won: {stats['games_won']}{RESET}")

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

            if real_board[cursor_idx] == SPACE:
                flood_fill(cursor_idx, real_board, visible_board, board_rows, board_cols)
            elif real_board[cursor_idx] != MINE:
                chording(cursor_idx, real_board, visible_board, board_rows, board_cols)

            if check_victory(real_board, visible_board):
                display_board(real_board, board_cols, board_rows, cell_w, cell_h, cursor_idx)
                message = f"{GREEN}Victory is yours!!!{RESET}"
                exit = True
            elif check_defeat(real_board, visible_board):
                display_board(real_board, board_cols, board_rows, cell_w, cell_h, cursor_idx)
                message = f"{RED}Ahhhhhhhhhhhhhhh{RESET}"
                exit = True

        elif key == "ESC":
            message = f"{GRAY}Exiting...{RESET}"
            exit = True

        save_game(
            player_name, 
            config["rows"], 
            config["cols"],
            real_board,
            visible_board,
            time.time())

    if message:
        print(f"\n{message}")

if __name__ == "__main__":
    hide_cursor()

    try:
        main()
    finally:
        show_cursor()