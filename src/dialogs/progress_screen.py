from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import LoadingIndicator


class ProgressScreen(ModalScreen[None]):
    DEFAULT_CSS = """
    ProgressScreen {
        align: center middle;
    }
    ProgressScreen LoadingIndicator {
        width: 40;
        height: 5;
        border: thick $primary;
        background: $panel;
    }
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield LoadingIndicator(self.message)
