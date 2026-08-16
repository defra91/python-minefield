from unittest.mock import patch

from python_minefield.game.math import (
    get_adjacent_indices,
    get_board_coords,
    is_float,
    random_int,
)


def test_random_int():
    """Test that random_int returns a value within the specified range."""
    with patch("random.randint", return_value=5) as mock_randint:
        result = random_int(1, 10)
        assert result == 5
        mock_randint.assert_called_once_with(1, 10)


def test_get_board_coords_top_left():
    """Test that get_board_coords returns the correct row and column for the top-left
    corner of the board."""
    row, col = get_board_coords(0, num_cols=5)
    assert (row, col) == (0, 0)


def test_get_board_coords_middle():
    """Test that get_board_coords returns
    the correct row and column for a middle index."""
    # Indice 6 in una griglia da 4 colonne -> riga 1, colonna 2
    row, col = get_board_coords(6, num_cols=4)
    assert (row, col) == (1, 2)


def test_get_board_coords_last_cell():
    """Test that get_board_coords returns
    the correct row and column for the last cell in a grid."""
    row, col = get_board_coords(8, num_cols=3)
    assert (row, col) == (2, 2)


def test_get_adjacent_indices_center():
    neighbors = get_adjacent_indices(idx=4, rows=3, cols=3)
    assert sorted(neighbors) == [0, 1, 2, 3, 5, 6, 7, 8]


def test_get_adjacent_indices_top_left_corner():
    neighbors = get_adjacent_indices(idx=0, rows=3, cols=3)
    assert sorted(neighbors) == [1, 3, 4]


def test_get_adjacent_indices_bottom_right_corner():
    neighbors = get_adjacent_indices(idx=8, rows=3, cols=3)
    assert sorted(neighbors) == [4, 5, 7]


def test_get_adjacent_indices_edge():
    neighbors = get_adjacent_indices(idx=1, rows=3, cols=3)
    assert sorted(neighbors) == [0, 2, 3, 4, 5]


# --- Test per is_float ---
def test_is_float_valid_values():
    assert is_float("123") is True
    assert is_float("3.14") is True
    assert is_float("-42.5") is True
    assert is_float("0.0") is True


def test_is_float_invalid_values():
    assert is_float("abc") is False
    assert is_float("12.3.4") is False
    assert is_float("") is False
    assert is_float("hello world") is False
