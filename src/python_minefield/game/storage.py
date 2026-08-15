# game/storage.py 

from pathlib import Path
import json
import time

from .core import check_defeat, check_victory

SAVES_DIR = Path.home() / ".python_minefield" / "saves"    

def ensure_saves_dir_exists():
    SAVES_DIR.mkdir(parents=True, exist_ok=True)

def get_player_filepath(player_name: str) -> Path:
    safe_name = (
        "".join(c for c in player_name if c.isalnum() or c in ("-", "_"))
        .rstrip()
        .lower()
    )
    if not safe_name:
        safe_name = "default_player"
    return SAVES_DIR / f"{safe_name}.json"

def save_game(
    player_name: str,
    rows: int,
    cols: int,
    real_board: list[str],
    visible_board: list[str],
    start_time: float
):
    ensure_saves_dir_exists()
    filepath = get_player_filepath(player_name)

    data = {}
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    elapsed = int(time.time() - start_time) if start_time else 0

    defeat = check_defeat(real_board, visible_board)
    victory = check_victory(real_board, visible_board)

    if "stats" not in data:
        data["stats"] = {"games_played": 0, "games_won": 0}

    data["player_name"] = player_name

    if defeat:
        data["stats"]["games_played"] += 1
    if victory:
        data["stats"]["games_won"] += 1
        data["stats"]["games_played"] += 1

    if victory or defeat:
        data["current_game"] = None
    else:
        data["current_game"] = {
            "rows": rows,
            "cols": cols,
            "start_time": start_time,
            "elapsed_seconds": elapsed,
            "real_board": real_board,
            "visible_board": visible_board,
        }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_game(player_name: str) -> dict | None:
    filepath = get_player_filepath(player_name)
    if not filepath.exists():
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        return None