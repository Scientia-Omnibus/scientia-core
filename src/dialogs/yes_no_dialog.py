"""Provides a dialog for getting a yes/no response from the user."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class YesNoDialog(ModalScreen[bool]):
    """A dialog for asking a user a yes/no question."""

    DEFAULT_CSS = """
    YesNoDialog {
        align: center middle;
    }

    YesNoDialog > Vertical {
        background: $panel;
        height: auto;
        width: auto;
        border: thick $primary;
    }

    YesNoDialog > Vertical > * {
        width: auto;
        height: auto;
    }

    YesNoDialog Static {
        width: auto;
    }

    YesNoDialog .spaced {
        padding: 1;
    }

    YesNoDialog #question {
        min-width: 100%;
        border-top: solid $primary;
        border-bottom: solid $primary;
    }

    YesNoDialog Button {
        margin-right: 1;
    }

    YesNoDialog #buttons {
        width: 100%;
        align-horizontal: right;
        padding-right: 1;
    }
    """

    BINDINGS = [
        Binding("left,up", "focus_previous", "", show=False),
        Binding("right,down", "focus_next", "", show=False),
        Binding("escape", "app.pop_screen", "", show=False),
    ]

    def __init__(
        self,
        title: str,
        question: str,
        yes_label: str = "Yes",
        no_label: str = "No",
        yes_first: bool = True,
    ) -> None:
        super().__init__()
        self._title = title
        self._question = question
        self._aye = yes_label
        self._naw = no_label
        self._aye_first = yes_first

    def compose(self) -> ComposeResult:
        with Vertical():
            with Center():
                yield Static(self._title, classes="spaced")
            yield Static(self._question, id="question", classes="spaced")
            with Horizontal(id="buttons"):
                aye = Button(self._aye, id="yes")
                naw = Button(self._naw, id="no")
                if self._aye_first:
                    aye.variant = "primary"
                    yield aye
                    yield naw
                else:
                    naw.variant = "primary"
                    yield naw
                    yield aye

    def on_mount(self) -> None:
        self.query(Button).first().focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")
