"""Provides the panes that go into the main navigation area."""

from widgets.navigation_panes.bookmarks import Bookmarks
from widgets.navigation_panes.history import History
from widgets.navigation_panes.local_files import LocalFiles
from widgets.navigation_panes.table_of_contents import TableOfContents

__all__ = [
    "Bookmarks",
    "History",
    "LocalFiles",
    "TableOfContents",
]
