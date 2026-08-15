# game/config.py

from .colors import RED, GRAY, RESET, BLUE_FLAG
    
SPACE        = f"{GRAY} {RESET}"
COVERED      = f"{GRAY}■{RESET}"
FLAG         = f"{BLUE_FLAG}⚑{RESET}"
MINE         = f"{RED}*{RESET}"

NUM_COLORS = {
    1: "\033[94m", 
    2: "\033[92m",
    3: "\033[93m", 
    4: "\033[34m",
    5: "\033[95m",
    6: "\033[96m",
    7: "\033[33m", 
    8: "\033[97m",
}

# Difficulties configuration

DIFFICULTIES = {
    "ROOKIE": {
        "rows": 6,
        "cols": 6,
        "percent": 0.08,
        "label": "Rookie",
    },
    "EASY": {
        "rows": 8,
        "cols": 8,
        "percent": 0.12,
        "label": "Easy",
    },
    "MEDIUM": {
        "rows": 10,
        "cols": 12,
        "percent": 0.16,
        "label": "Medium",
    },
    "HARD": {
        "rows": 12,
        "cols": 16,
        "percent": 0.20,
        "label": "Hard",
    },
    "EXTREME": {
        "rows": 16,
        "cols": 20,
        "percent": 0.25,
        "label": "Extreme",
    },
}