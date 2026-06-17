from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList

from src.data.data_directory import data_directory


class DirectoryPicker(ModalScreen[Path]):
    """A modal dialog for selecting a knowledge directory."""

    DEFAULT_CSS = """
    DirectoryPicker {
        align: center middle;
    }

    DirectoryPicker > Vertical {
        background: $panel;
        height: auto;
        width: auto;
        border: thick $primary;
    }

    DirectoryPicker > Vertical > * {
        width: auto;
        height: auto;
    }

    DirectoryPicker Label {
        margin-left: 2;
    }

    DirectoryPicker OptionList {
        width: 40;
        margin: 1;
    }

    DirectoryPicker Button {
        margin-right: 1;
    }

    DirectoryPicker #buttons {
        width: 100%;
        align-horizontal: right;
        padding-right: 1;
    }
    """
    """The default styling for the directory picker dialog."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "", show=False),
    ]
    """Bindings for the dialog."""

    def __init__(self) -> None:
        super().__init__()
        self.paths = [item.name for item in data_directory().iterdir() if item.is_dir()]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Select from existing:")
            yield OptionList(*self.paths, id="choices")
            with Horizontal(id="buttons"):
                yield Button("Cancel", id="cancel")
                yield Button("OK", id="ok", variant="primary")

    @on(Button.Pressed, "#cancel")
    def cancel_choice(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#ok")
    def accept_choice(self) -> None:
        if self.query_one(OptionList).highlighted is not None:
            self.dismiss(
                data_directory() / self.paths[self.query_one(OptionList).highlighted]
            )
