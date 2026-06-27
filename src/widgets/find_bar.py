from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Checkbox, Input, Label


class FindBar(Horizontal):
    """Inline find bar docked to the top of the viewer."""

    DEFAULT_CSS = """
    FindBar {
        dock: top;
        display: none;
        height: 3;
        width: 100%;
        background: $panel;
        border-bottom: solid $primary;
        padding: 0 1;
        layout: horizontal;
        align: left middle;
    }

    FindBar .find-label {
        width: auto;
        padding-right: 1;
        color: $text 50%;
    }

    FindBar #find-input {
        width: 1fr;
        margin: 0 1 0 0;
    }

    FindBar #case-sensitive {
        width: auto;
        margin-right: 1;
    }

    FindBar Button {
        min-width: 3;
        margin-right: 1;
    }

    FindBar .find-status {
        width: auto;
        min-width: 10;
        color: $text 50%;
        text-align: right;
    }
    """

    class FindNext(Message):
        def __init__(self, query: str, case_sensitive: bool) -> None:
            super().__init__()
            self.query = query
            self.case_sensitive = case_sensitive

    class FindPrevious(Message):
        def __init__(self, query: str, case_sensitive: bool) -> None:
            super().__init__()
            self.query = query
            self.case_sensitive = case_sensitive

    class Closed(Message):
        pass

    def compose(self) -> ComposeResult:
        yield Label("Find:", classes="find-label")
        yield Input(placeholder="Find in document...", id="find-input")
        yield Checkbox("Aa", id="case-sensitive", button_first=True)
        yield Button("▲", id="find-prev")
        yield Button("▼", id="find-next")
        yield Label("", id="find-status", classes="find-status")

    def show_find(self) -> None:
        self.display = True
        self.query_one("#find-input", Input).focus()

    def hide(self) -> None:
        self.display = False
        self.query_one("#find-status", Label).update("")
        self.post_message(FindBar.Closed())

    def set_status(self, text: str) -> None:
        self.query_one("#find-status", Label).update(text)

    def _query(self) -> str:
        return self.query_one("#find-input", Input).value

    def _case_sensitive(self) -> bool:
        return bool(self.query_one("#case-sensitive", Checkbox).value)

    def _post_find_next(self) -> None:
        self.post_message(FindBar.FindNext(self._query(), self._case_sensitive()))
        self.query_one("#find-input", Input).focus()

    def _post_find_previous(self) -> None:
        self.post_message(FindBar.FindPrevious(self._query(), self._case_sensitive()))
        self.query_one("#find-input", Input).focus()

    @on(Button.Pressed, "#find-prev")
    def _on_find_prev(self) -> None:
        self._post_find_previous()

    @on(Button.Pressed, "#find-next")
    def _on_find_next(self) -> None:
        self._post_find_next()

    @on(Input.Submitted, "#find-input")
    def _on_find_submitted(self) -> None:
        self._post_find_next()

    def on_key(self, event) -> None:
        if event.key == "shift+enter":
            event.stop()
            event.prevent_default()
            self._post_find_previous()
        elif event.key == "escape":
            event.stop()
            self.hide()
