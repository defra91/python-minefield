import random
import sys
from collections import deque

from .math import get_board_coords, NEIGHBORS_OFFSET
from .math import random_int, get_adjacent_indices, get_board_coords
from .config import FLAG, FLAG, MINE, NUM_COLORS, SPACE, COVERED, DIFFICULTIES
from .colors import BOLD, CURSOR_STYLE, GRAY, RESET
from .terminal import get_key, hide_cursor, show_cursor

def count_adjacent_mines(i, board, board_rows, board_cols):
    r, c = get_board_coords(i, board_cols)
    mine_cnt = 0

    for dr, dc in NEIGHBORS_OFFSET:
        nr, nc = r + dr, c + dc

        if 0 <= nr < board_rows and 0 <= nc < board_cols:
            neighbor_index = nr * board_cols + nc
            mine_cnt += board[neighbor_index] == MINE

    return mine_cnt

def flood_fill(start_i, real_board, visible_board, board_rows, board_cols):
    queue = deque([start_i])

    visited = {start_i}

    while queue:
        i = queue.popleft()

        visible_board[i] = real_board[i]

        if real_board[i] != SPACE:
            continue

        r, c = get_board_coords(i, board_cols)

        for dr, dc in NEIGHBORS_OFFSET:
            nr, nc = r + dr, c + dc

            if 0 <= nr < board_rows and 0 <= nc < board_cols:
                neighbor_idx = nr * board_cols + nc

                if (
                    neighbor_idx not in visited
                    and visible_board[neighbor_idx] == COVERED
                ):
                    visited.add(neighbor_idx)
                    queue.append(neighbor_idx)

def select_difficulty() -> str:
    keys = list(DIFFICULTIES.keys())
    cursor = 0 

    while True:
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(f"{BOLD}=== SELECT DIFFICULTY ==={RESET}\n\n")

        for i, key in enumerate(keys):
            label = DIFFICULTIES[key]["label"]

            if i == cursor:
                sys.stdout.write(f"  {CURSOR_STYLE} > {label} < {RESET}\n")
            else:
                sys.stdout.write(f"    {GRAY}{label}{RESET}\n")

        sys.stdout.write(
            f"\n{GRAY}Use UP/DOWN arrows and press ENTER to confirm.{RESET}\n"
        )
        sys.stdout.flush()

        action = get_key()

        if action == "UP" and cursor > 0:
            cursor -= 1
        elif action == "DOWN" and cursor < len(keys) - 1:
            cursor += 1
        elif action == "ENTER":
            return keys[cursor]

def check_victory(real_board, visible_board) -> bool:
    for i, cell in enumerate(real_board):
        if cell != MINE:
            if visible_board[i] in (COVERED, FLAG):
                return False

    return True

def check_defeat(real_board, visible_board) -> bool:
    defeat = False
    for i, cell in enumerate(real_board):
        vcell = visible_board[i]
        if (cell == MINE and vcell == MINE):
            defeat = True
        
    return defeat

def get_player_name() -> str:
    show_cursor()
    player_name = input("Insert your name: ").strip()
    hide_cursor()
    return player_name if player_name else "Player"

def init_game(config):
    real_board = []
    visible_board = []
    
    board_size = config["rows"] * config["cols"]
    mines_cnt = max(1, round(board_size * config["percent"]))

    for i in range(config["cols"]):
        for _ in range(config["rows"]):
            real_board.append(SPACE)
            visible_board.append(COVERED)

    start_point = random_int(0, board_size - 1)
    forbidden_points = get_adjacent_indices(start_point, config["rows"], config["cols"])
    forbidden_points.append(start_point) 

    allowed_indices = [i for i in range(board_size) if i not in forbidden_points]

    mine_indices = random.sample(allowed_indices, mines_cnt)
    for idx in mine_indices:
        real_board[idx] = MINE

    for i, cell in enumerate(real_board):
        if cell == MINE:
            continue

        mines = count_adjacent_mines(i, real_board, config["rows"], config["cols"])

        if mines > 0:
            color = NUM_COLORS[mines]
            real_board[i] = f"{color}{mines}{RESET}"
        else:
            real_board[i] = SPACE

    flood_fill(start_point, real_board, visible_board, config["rows"], config["cols"])

    return real_board, visible_board
