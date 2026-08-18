import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from python_minefield.game.storage import (
    ensure_saves_dir_exists,
    get_player_filepath,
    load_game,
    save_game,
)

fake_home = Path("/my/home")


def test_ensure_saves_dir_exists():
    # Arrange
    with (
        patch("python_minefield.game.storage.Path.home", return_value=fake_home),
        patch("pathlib.Path.mkdir") as mock_mkdir,
    ):
        # Act
        ensure_saves_dir_exists()

        # Assert
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


@pytest.mark.parametrize(
    "input_name, expected_filename",
    [
        ("TestPlayer", "testplayer.json"),
        ("Mario Rossi", "mariorossi.json"),
        ("Player#123!🎮", "player123.json"),
        ("User_Name-99", "user_name-99.json"),
        ("", "default_player.json"),
        ("   ", "default_player.json"),
        ("!!!", "default_player.json"),
    ],
)
def test_get_player_filepath(input_name: str, expected_filename: str):
    # Arrange
    fake_saves_dir = Path("/my/home/.python_minefield/saves")
    expected_path = fake_saves_dir / expected_filename

    with patch("python_minefield.game.storage.SAVES_DIR", fake_saves_dir):
        # Act
        result = get_player_filepath(input_name)

        # Assert
        assert result == expected_path


@pytest.mark.parametrize(
    "player_name",
    [
        ("Mario Rossi",),
    ],
)
def test_save_game(player_name: str, rows: int = 5, cols: int = 5):
    # Arrange
    filepath = Path("/my/home/.python_minefield/saves/player.json")
    start_time = 0

    mock_player_data = {
        "name": player_name,
        "stats": {
            "games_played": 10,
            "games_won": 5,
        },
    }

    mock_json_file_content = json.dumps(mock_player_data)

    mock_file = mock_open(read_data=mock_json_file_content)

    real_board = ["*"] * (rows * cols)
    visible_board = [" "] * (rows * cols)

    with (
        patch("python_minefield.game.storage.ensure_saves_dir_exists") as _,
        patch(
            "python_minefield.game.storage.get_player_filepath", return_value=filepath
        ),
        patch.object(Path, "exists", return_value=True),
        patch("python_minefield.game.storage.open", mock_file),
    ):
        # Act
        save_game(player_name, rows, cols, real_board, visible_board, start_time)


def test_load_game():
    # Arrange
    player_name = "TestPlayer"
    filepath = Path("/my/home/.python_minefield/saves/testplayer.json")
    json_data = {
        "name": player_name,
        "stats": {
            "games_played": 10,
            "games_won": 5,
        },
    }
    json_str = json.dumps(json_data)
    with (
        patch(
            "python_minefield.game.storage.get_player_filepath", return_value=filepath
        ) as mock_get_path,
        patch.object(Path, "exists", return_value=True),
        patch("python_minefield.game.storage.open", mock_open(read_data=json_str)),
    ):
        # Act
        result = load_game(player_name)

        # Assert
        assert result == json_data
        mock_get_path.assert_called_once_with(player_name)


def test_load_game_file_not_found():
    # Arrange
    player_name = "TestPlayer"
    filepath = Path("/my/home/.python_minefield/saves/testplayer.json")
    with (
        patch(
            "python_minefield.game.storage.get_player_filepath", return_value=filepath
        ),
        patch.object(Path, "exists", return_value=False),
    ):
        # Act
        result = load_game(player_name)

        # Assert
        assert result is None


def test_load_game_corrupted_json_returns_none():
    # Arrange
    player_name = "TestPlayer"
    filepath = Path("/my/home/.python_minefield/saves/testplayer.json")
    invalid_json_content = "{ invalid json content... "

    with (
        patch(
            "python_minefield.game.storage.get_player_filepath", return_value=filepath
        ) as _,
        patch.object(Path, "exists", return_value=True),
        patch(
            "python_minefield.game.storage.open",
            mock_open(read_data=invalid_json_content),
        ),
    ):
        # Act
        result = load_game(player_name)

        # Assert
        assert result is None
