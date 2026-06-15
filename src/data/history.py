from __future__ import annotations

from json import JSONEncoder, dumps, loads
from pathlib import Path
from typing import Any

from src.data.data_directory import data_directory


def history_file() -> Path:
    return data_directory() / "history.json"


class HistoryEncoder(JSONEncoder):
    def default(self, o: object) -> Any:
        return str(o) if isinstance(o, Path) else o


def save_history(history: list[Path]) -> None:
    history_file().write_text(dumps(history, indent=4, cls=HistoryEncoder))


def load_history() -> list[Path]:
    return (
        [Path(location) for location in loads(history.read_text())]
        if (history := history_file()).exists()
        else []
    )
