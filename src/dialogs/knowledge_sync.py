from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, OptionList


class KnowledgeSync(ModalScreen[str]):
    """A modal dialog for syncing knowledge base repositories."""

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

    def __init__(self) -> None:
        super().__init__()
        self.sciences = ["formal-sciences"]

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
        option_list = self.query_one(OptionList)
        if (
            highlighted := option_list.highlighted
        ) is not None and 0 <= highlighted < len(self.sciences):
            self.dismiss(self.sciences[highlighted])
