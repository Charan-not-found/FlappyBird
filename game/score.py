"""Reads and writes the high score to a plain text file next to the game."""

from . import constants as C


def load_highscore() -> int:
    try:
        return int(C.HIGHSCORE_FILE.read_text().strip())
    except (OSError, ValueError):
        return 0


def save_highscore(score: int) -> None:
    try:
        C.HIGHSCORE_FILE.write_text(str(int(score)))
    except OSError as exc:
        print(f"[score] could not save high score: {exc}")
