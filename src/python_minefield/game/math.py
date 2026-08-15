# game/math.py

import random

NEIGHBORS_OFFSET = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

def random_int(min, max):
    """Extracts and returns a random integer between the min and max"""
    return random.randint(min, max)

def get_board_coords(index: int, num_cols: int) -> tuple[int, int]:
    row = index // num_cols
    col = index % num_cols
    return row, col

def get_adjacent_indices(idx: int, rows: int, cols: int) -> list[int]:
    r = idx // cols
    c = idx % cols

    adjacent = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                adjacent.append(nr * cols + nc)

    return adjacent

def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False