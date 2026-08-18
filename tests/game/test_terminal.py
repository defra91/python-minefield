from unittest.mock import patch

import pytest

from python_minefield.game.terminal import (
    clear_screen,
    get_key,
    hide_cursor,
    normalize_cell_size,
    show_cursor,
)


def test_hide_cursor():
    # Arrange
    with (
        patch("sys.stdout.write") as mock_write,
        patch("sys.stdout.flush") as mock_flush,
    ):
        # Act
        hide_cursor()

        # Assert
        mock_write.assert_called_once_with("\033[?25l")
        mock_flush.assert_called_once()


def test_show_cursor():
    # Arrange
    with (
        patch("sys.stdout.write") as mock_write,
        patch("sys.stdout.flush") as mock_flush,
    ):
        # Act
        show_cursor()

        # Assert
        mock_write.assert_called_once_with("\033[?25h")
        mock_flush.assert_called_once()


def test_clear_screen():
    # Arrange
    with (
        patch("sys.stdout.write") as mock_write,
        patch("sys.stdout.flush") as mock_flush,
    ):
        # Act
        clear_screen()

        # Assert
        mock_write.assert_called_once_with("\033[2J\033[H\033[?25l")
        mock_flush.assert_called_once()


def get_terminal_width():
    # Arrange
    with patch("shutil.get_terminal_size") as mock_get_terminal_size:
        mock_get_terminal_size.return_value = (100, 20)

        # Act
        width = get_terminal_width()

        # Assert
        assert width == 100
        mock_get_terminal_size.assert_called_once_with((80, 20))


@pytest.mark.parametrize(
    "cell_size, expected",
    [
        (1, 1),
        (2, 3),
        (3, 3),
        (4, 5),
        (10, 11),
    ],
)
def test_normalize_cell_size_valid_inputs(cell_size: int, expected: int):
    assert normalize_cell_size(cell_size) == expected


@pytest.mark.parametrize(
    "invalid_type_input",
    [
        "3",  # String
        3.0,  # Float
        None,  # NoneType
        [2],  # List
        True,  # Bool (inherits from int in Python, but is invalid for cell dimensions)
    ],
)
def test_normalize_cell_size_raises_type_error(invalid_type_input):
    with pytest.raises(TypeError):
        normalize_cell_size(invalid_type_input)


@pytest.mark.parametrize(
    "invalid_value_input",
    [
        0,  # Zero
        -1,  # Negative odd number
        -2,  # Negative even number
        -100,  # Large negative number
    ],
)
def test_normalize_cell_size_raises_value_error(invalid_value_input: int):
    with pytest.raises(ValueError):
        normalize_cell_size(invalid_value_input)


@pytest.mark.parametrize(
    "input_chars, expected_key",
    [
        (["\x1b", "[", "A"], "UP"),
        (["\x1b", "[", "B"], "DOWN"),
        (["\x1b", "[", "D"], "LEFT"),
        (["\x1b", "[", "C"], "RIGHT"),
        (["\x1b", "O", "H"], "ESC"),
        (["\r"], "ENTER"),
        (["\n"], "ENTER"),
        ([" "], "SPACE"),
        (["f"], "FLAG"),
        (["F"], "FLAG"),
        (["q"], "ESC"),
        (["Q"], "ESC"),
        (["x"], None),
    ],
)
def test_get_key(input_chars: list[str], expected_key: str | None):
    # Arrange
    module_path = "python_minefield.game.terminal"
    with (
        patch(f"{module_path}.sys.stdin.fileno", return_value=0),
        patch(f"{module_path}.termios.tcgetattr", return_value=["fake_settings"]),
        patch(f"{module_path}.termios.tcsetattr") as mock_tcsetattr,
        patch(f"{module_path}.tty.setraw") as mock_setraw,
        patch(f"{module_path}.sys.stdout.write"),
        patch(f"{module_path}.sys.stdout.flush"),
        patch(f"{module_path}.sys.stdin.read", side_effect=input_chars) as mock_read,
    ):
        # Act
        key = get_key()

        # Assert
        assert key == expected_key

        mock_setraw.assert_called_once_with(0)
        mock_tcsetattr.assert_called_once()

        assert mock_read.call_count == len(input_chars)
