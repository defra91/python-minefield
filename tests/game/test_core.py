import pytest

from python_minefield.game.core import (
    count_adjacent_mines,
)

ADJACENT_MINES_TEST_CASES = {
    ("#M#", "#X#", "###"): 1,
    ("MMM", "MXM", "MMM"): 8,
    ("XM#", "M##", "###"): 2,
    ("###", "#M#", "##X"): 1,
    ("#M#M", "X#M#", "####"): 1,
    ("###", "#X#", "###"): 0,
}


@pytest.mark.parametrize("layout, expected_mines", ADJACENT_MINES_TEST_CASES.items())
def test_count_adjacent_mines(
    board_parser, layout: tuple[str, ...], expected_mines: int
):
    # Arrange
    flat_board, rows, cols, target_index = board_parser(layout)

    # Act
    result = count_adjacent_mines(target_index, flat_board, rows, cols)

    # Assert
    assert result == expected_mines
