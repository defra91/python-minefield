import pytest

from python_minefield.game.config import (
    COVERED,
    MINE,
    SPACE,
)


@pytest.fixture
def board_parser():
    def _parse(layout: tuple[str, ...] | list[str]) -> tuple[list, int, int, int]:
        rows = len(layout)
        cols = len(layout[0])
        flat_board = []
        target_index = None

        for r, row_str in enumerate(layout):
            for c, char in enumerate(row_str):
                index = r * cols + c
                if char == "X":
                    target_index = index
                    flat_board.append(SPACE)
                elif char in ("M", "*"):
                    flat_board.append(MINE)
                else:
                    # Tutti i caratteri non mina ('.', '#', ecc.) diventano SPACE
                    flat_board.append(SPACE)

        if target_index is None:
            raise ValueError(
                "The ASCII layout must contain exactly one 'X' target cell."
            )

        return flat_board, rows, cols, target_index

    return _parse


def parse_flood_fill_layout(
    real_layout: tuple[str, ...],
    expected_visible_layout: tuple[str, ...],
    covered_char: str = "#",
) -> tuple[list, list, list, int, int, int]:
    rows = len(real_layout)
    cols = len(real_layout[0])

    real_board = []
    expected_visible_board = []
    initial_visible_board = [COVERED] * (rows * cols)
    start_i = None

    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            real_char = real_layout[r][c]
            exp_char = expected_visible_layout[r][c]

            # 1. Parse Real Board & Start Position 'X'
            if real_char == "X":
                start_i = idx
                real_board.append(SPACE)
            elif real_char == ".":
                real_board.append(SPACE)
            elif real_char == "M":
                real_board.append(MINE)
            else:
                # Numbers '1', '2', etc.
                real_board.append(real_char)

            # 2. Parse Expected Visible Board
            if exp_char == covered_char:
                expected_visible_board.append(COVERED)
            elif exp_char == ".":
                expected_visible_board.append(SPACE)
            else:
                expected_visible_board.append(exp_char)

    if start_i is None:
        raise ValueError(
            "Real layout must contain exactly one 'X' for the start position."
        )

    return (
        real_board,
        initial_visible_board,
        expected_visible_board,
        rows,
        cols,
        start_i,
    )
