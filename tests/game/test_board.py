from unittest.mock import MagicMock, patch

from python_minefield.game.board import (
    BORDER_HORIZ,
    BORDER_VERT,
    DIVIDER_BOTTOM,
    DIVIDER_MID,
    DIVIDER_TOP,
    L_CORNER_BOTTOM,
    L_CORNER_TOP,
    L_DIVIDER_MID,
    R_CORNER_BOTTOM,
    R_CORNER_TOP,
    R_DIVIDER_MID,
    board_row_bottom,
    board_row_central,
    board_row_central_divider_mid,
    board_row_top,
    display_board,
    render_board,
)
from python_minefield.game.config import SPACE


def test_board_row_top_basic():
    # Arrange
    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 2

        # Act
        result = board_row_top(cell_cnt=3, cell_size=2)

        expected = (
            f"{L_CORNER_TOP}"
            f"{BORDER_HORIZ * 2}{DIVIDER_TOP}"
            f"{BORDER_HORIZ * 2}{DIVIDER_TOP}"
            f"{BORDER_HORIZ * 2}"
            f"{R_CORNER_TOP}"
        )

        # Assert
        assert result == expected
        mock_normalize.assert_called_once_with(2)


def test_board_row_bottom():
    # Arrange
    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 3

        # Act
        result = board_row_bottom(cell_cnt=2, cell_size=3)

        expected = (
            f"{L_CORNER_BOTTOM}"
            f"{BORDER_HORIZ * 3}{DIVIDER_BOTTOM}"
            f"{BORDER_HORIZ * 3}"
            f"{R_CORNER_BOTTOM}"
        )

        # Assert
        assert result == expected
        mock_normalize.assert_called_once_with(3)


def test_board_row_central_with_null_contents():
    # Arrange
    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 3

        # Act
        result = board_row_central(cell_size=4, contents=None)

        expected = f"{BORDER_VERT}{BORDER_VERT}"

        # Assert
        assert result == expected
        mock_normalize.assert_called_once_with(4)


def test_board_row_central():
    # Arrange
    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 3

        # Act
        result = board_row_central(
            cell_size=3, contents=["X", "O"], default_cell_value="*"
        )

        expected = f"{BORDER_VERT}*X*{BORDER_VERT}*O*{BORDER_VERT}"

        # Assert
        assert result == expected
        mock_normalize.assert_called_once_with(3)


def test_board_row_central_divider_mid():
    # Arrange

    cell_cnt = 3
    cell_size = 4

    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 3

        # Act
        result = board_row_central_divider_mid(cell_cnt, cell_size)

        # Assert
        expected = (
            f"{L_DIVIDER_MID}"
            f"{BORDER_HORIZ * (cell_size - 1)}{DIVIDER_MID}"
            f"{BORDER_HORIZ * (cell_size - 1)}{DIVIDER_MID}"
            f"{BORDER_HORIZ * (cell_size - 1)}{R_DIVIDER_MID}"
        )
        assert result == expected
        mock_normalize.assert_called_once_with(cell_size)


def test_display_board():
    # Arrange
    board = [1, 2, "", SPACE]

    cols = 2
    rows = 2
    cell_w = 3
    cell_h = 3
    cursor_idx = 0

    with patch("python_minefield.game.terminal.normalize_cell_size") as mock_normalize:
        mock_normalize.return_value = 3

        # Act
        result = display_board(board, cols, rows, cell_w, cell_h, cursor_idx)

        assert isinstance(result, str)
        assert "1" in result
        assert "2" in result


def test_render_board():
    # Arrange
    board = [1, 2, "", SPACE]

    cols = 2
    rows = 2
    cell_w = 3
    cell_h = 3
    cursor_idx = 0
    expected_buffer = "mocked_buffer_content"

    with (
        patch(
            "python_minefield.game.board.display_board", return_value=expected_buffer
        ) as mock_display,
        patch("sys.stdout", new_callable=MagicMock) as mock_stdout,
    ):
        # Act
        render_board(board, cols, rows, cell_w, cell_h, cursor_idx)

        # Assert
        mock_display.assert_called_once_with(
            board, cols, rows, cell_w, cell_h, cursor_idx
        )

        mock_stdout.write.assert_called_once_with(expected_buffer)
        mock_stdout.flush.assert_called_once()
