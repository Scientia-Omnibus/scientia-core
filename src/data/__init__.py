"""Provides tools for saving and loading application data."""

from src.data.bookmarks import Bookmark, load_bookmarks, save_bookmarks
from src.data.config import Config, load_config, save_config
from src.data.history import load_history, save_history

__all__ = [
    "Bookmark",
    "Config",
    "load_bookmarks",
    "load_config",
    "load_history",
    "save_bookmarks",
    "save_config",
    "save_history",
]
