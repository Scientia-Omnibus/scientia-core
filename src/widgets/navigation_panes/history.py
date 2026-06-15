from __future__ import annotations

from functools import partial
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from src.dialogs import YesNoDialog
from src.widgets.navigation_panes.navigation_pane import NavigationPane


class Entry(Option):
    def __init__(self, history_id: int, location: Path) -> None:
        super().__init__(self._as_prompt(location))
        self.history_id = history_id
        self.location = location

    @staticmethod
    def _as_prompt(location: Path) -> Text:
        return Text.from_markup(
            f":page_facing_up: [bold]{location.name}[/]\n[dim]{location.parent}[/]",
            overflow="ellipsis",
        )


class History(NavigationPane):
    DEFAULT_CSS = """
    History {
        height: 100%;
    }

    History > OptionList {
        background: $panel;
        border: none;
        height: 1fr;
    }

    History > OptionList:focus {
        border: none;
    }
    """

    BINDINGS = [
        Binding("delete", "delete", "Delete the history item"),
        Binding("backspace", "clear", "Clean the history"),
    ]

    def __init__(self) -> None:
        super().__init__("History")

    def compose(self) -> ComposeResult:
        yield OptionList()

    def set_focus_within(self) -> None:
        self.query_one(OptionList).focus(scroll_visible=False)

    def update_from(self, locations: list[Path]) -> None:
        option_list = self.query_one(OptionList).clear_options()
        for history_id, location in reversed(list(enumerate(locations))):
            option_list.add_option(Entry(history_id, location))

    class Goto(Message):
        def __init__(self, location: Path) -> None:
            super().__init__()
            self.location = location

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        event.stop()
        assert isinstance(event.option, Entry)
        self.post_message(self.Goto(event.option.location))

    class Delete(Message):
        def __init__(self, history_id: int) -> None:
            super().__init__()
            self.history_id = history_id

    def delete_history(self, history_id: int, delete_it: bool) -> None:
        if delete_it:
            self.post_message(self.Delete(history_id))

    def action_delete(self) -> None:
        history = self.query_one(OptionList)
        if (item := history.highlighted) is not None:
            assert isinstance(entry := history.get_option_at_index(item), Entry)
            self.app.push_screen(
                YesNoDialog(
                    "Delete history entry?",
                    "Are you sure you want to delete the history entry?",
                ),
                partial(self.delete_history, entry.history_id),
            )

    class Clear(Message):
        pass

    def clear_history(self, clear_it: bool) -> None:
        if clear_it:
            self.post_message(self.Clear())

    def action_clear(self) -> None:
        self.app.push_screen(
            YesNoDialog(
                "Clear history?",
                "Are you sure you want to clear everything out of history?",
            ),
            self.clear_history,
        )
