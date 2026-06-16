from __future__ import annotations

from pathlib import Path
from typing import Iterable

from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import DirectoryTree

from src.utils import maybe_markdown
from src.widgets.navigation_panes.navigation_pane import NavigationPane


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        try:
            return [
                path
                for path in paths
                if not path.name.startswith(".")
                and path.is_dir()
                or (path.is_file() and maybe_markdown(path))
            ]
        except PermissionError:
            return []


class LocalFiles(NavigationPane):
    DEFAULT_CSS = """
    LocalFiles {
        height: 100%;
    }

    LocalFiles > DirectoryTree {
        background: $panel;
        width: 1fr;
    }

    LocalFiles > DirectoryTree:focus .tree--cursor, LocalFiles > DirectoryTree .tree--cursor {
        background: $accent 50%;
        color: $text;
    }
    """

    def __init__(self) -> None:
        super().__init__("Local")

    def compose(self) -> ComposeResult:
        yield FilteredDirectoryTree(Path("~").expanduser())

    def chdir(self, path: Path) -> None:
        self.query_one(FilteredDirectoryTree).path = path

    def set_focus_within(self) -> None:
        self.query_one(DirectoryTree).focus(scroll_visible=False)

    class Goto(Message):
        def __init__(self, location: Path) -> None:
            super().__init__()
            self.location = location

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()
        self.post_message(self.Goto(Path(event.path)))
