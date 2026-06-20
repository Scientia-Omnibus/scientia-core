from __future__ import annotations

from json import JSONEncoder, dumps, loads
from pathlib import Path
from typing import Any, NamedTuple

from data.data_directory import data_directory


class Bookmark(NamedTuple):
    title: str
    location: Path


def bookmarks_file() -> Path:
    return data_directory() / "bookmarks.json"


class BookmarkEncoder(JSONEncoder):
    def default(self, o: object) -> Any:
        return str(o) if isinstance(o, Path) else o


def save_bookmarks(bookmarks: list[Bookmark]) -> None:
    bookmarks_file().write_text(dumps(bookmarks, indent=4, cls=BookmarkEncoder))


def load_bookmarks() -> list[Bookmark]:
    return (
        [
            Bookmark(title, Path(location))
            for (title, location) in loads(bookmarks.read_text())
        ]
        if (bookmarks := bookmarks_file()).exists()
        else []
    )
