from __future__ import annotations

from functools import partial
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from src.data import Bookmark, load_bookmarks, save_bookmarks
from src.dialogs import InputDialog, YesNoDialog
from src.widgets.navigation_panes.navigation_pane import NavigationPane


class Entry(Option):
    def __init__(self, bookmark: Bookmark) -> None:
        super().__init__(self._as_prompt(bookmark))
        self.bookmark = bookmark

    @staticmethod
    def _as_prompt(bookmark: Bookmark) -> Text:
        return Text.from_markup(
            f":page_facing_up: [bold]{bookmark.title}[/]\n[dim]{bookmark.location}[/]",
            overflow="ellipsis",
        )


class Bookmarks(NavigationPane):
    DEFAULT_CSS = """
    Bookmarks {
        height: 100%;
    }

    Bookmarks > OptionList {
        background: $panel;
        border: none;
        height: 1fr;
    }

    Bookmarks > OptionList:focus {
        border: none;
    }
    """

    BINDINGS = [
        Binding("delete", "delete", "Delete the bookmark"),
        Binding("r", "rename", "Rename the bookmark"),
    ]

    def __init__(self) -> None:
        super().__init__("Bookmarks")
        self._bookmarks: list[Bookmark] = load_bookmarks()

    def compose(self) -> ComposeResult:
        yield OptionList(*[Entry(bookmark) for bookmark in self._bookmarks])

    def set_focus_within(self) -> None:
        self.query_one(OptionList).focus(scroll_visible=False)

    def _bookmarks_updated(self) -> None:
        bookmarks = self.query_one(OptionList)
        old_position = bookmarks.highlighted
        bookmarks.clear_options()
        for bookmark in self._bookmarks:
            bookmarks.add_option(Entry(bookmark))
        save_bookmarks(self._bookmarks)
        bookmarks.highlighted = old_position

    def add_bookmark(self, title: str, location: Path) -> None:
        self._bookmarks.append(Bookmark(title, location))
        self._bookmarks = sorted(self._bookmarks, key=lambda bookmark: bookmark.title)
        self._bookmarks_updated()

    class Goto(Message):
        def __init__(self, bookmark: Bookmark) -> None:
            super().__init__()
            self.bookmark = bookmark

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        event.stop()
        assert isinstance(event.option, Entry)
        self.post_message(self.Goto(event.option.bookmark))

    def delete_bookmark(self, bookmark: int, delete_it: bool) -> None:
        if delete_it:
            del self._bookmarks[bookmark]
            self._bookmarks_updated()

    def action_delete(self) -> None:
        if (bookmark := self.query_one(OptionList).highlighted) is not None:
            self.app.push_screen(
                YesNoDialog(
                    "Delete bookmark",
                    "Are you sure you want to delete the bookmark?",
                ),
                partial(self.delete_bookmark, bookmark),
            )

    def rename_bookmark(self, bookmark: int, new_name: str) -> None:
        self._bookmarks[bookmark] = Bookmark(
            new_name, self._bookmarks[bookmark].location
        )
        self._bookmarks_updated()

    def action_rename(self) -> None:
        if (bookmark := self.query_one(OptionList).highlighted) is not None:
            self.app.push_screen(
                InputDialog(
                    "Bookmark title:",
                    self._bookmarks[bookmark].title,
                ),
                partial(self.rename_bookmark, bookmark),
            )
