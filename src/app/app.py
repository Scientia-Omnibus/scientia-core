from textual.app import App

from src.data import load_config
from src.screens import Main


class ScientiaCore(App[None]):
    TITLE = "Scientia Omnibus"
    ENABLE_COMMAND_PALETTE = True

    def __init__(self) -> None:
        super().__init__()
        self.dark = not load_config().light_mode

    def on_mount(self) -> None:
        self.push_screen(Main())


def run() -> None:
    ScientiaCore().run()
