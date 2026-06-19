from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList

from src.data.data_directory import data_directory


class KnowledgeSync(ModalScreen[Path]):
    """A modal dialog for selecting a knowledge directory."""

    DEFAULT_CSS = """
    KnowledgeSync {
        align: center middle;
    }

    KnowledgeSync > Vertical {
        background: $panel;
        height: auto;
        width: auto;
        border: thick $primary;
    }

    KnowledgeSync > Vertical > * {
        width: auto;
        height: auto;
    }

    KnowledgeSync Label {
        margin-left: 2;
    }

    KnowledgeSync OptionList {
        width: 40;
        margin: 1;
    }

    KnowledgeSync Button {
        margin-right: 1;
    }

    KnowledgeSync #buttons {
        width: 100%;
        align-horizontal: right;
        padding-right: 1;
    }
    """

    BINDINGS = [
        Binding("escape", "app.pop_screen", "", show=False),
    ]
    """Bindings for the dialog."""

    def __init__(self) -> None:
        super().__init__()
        self.sciences = [
            "humanities-sciences",
            "social-sciences",
            "natural-sciences",
            "formal-sciences",
        ]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Select from existing to update or download:")
            yield OptionList(*self.sciences, id="choices")
            with Horizontal(id="buttons"):
                yield Button("Cancel", id="cancel")
                yield Button("OK", id="ok", variant="primary")

    @on(Button.Pressed, "#cancel")
    def cancel_choice(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#ok")
    def accept_choice(self) -> None:
        if self.query_one(OptionList).highlighted is not None:
            self.dismiss(self.sciences[self.query_one(OptionList).highlighted])
