from textual.app import App

from data import load_config
from screens import Main


class ScientiaCore(App[None]):
    TITLE = "Scientia Omnibus"
    ENABLE_COMMAND_PALETTE = False

    DEFAULT_CSS = """
    ScientiaCore {
        background: $background;
        color: $foreground;
    }

    Scrollbar {
        scrollbar-color: $scrollbar;
        scrollbar-background: $scrollbar-background;
        scrollbar-color-hover: $scrollbar-hover;
        scrollbar-color-active: $scrollbar-active;
        scrollbar-corner-color: $scrollbar-corner-color;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.dark = not load_config().light_mode

    def on_mount(self) -> None:
        self.theme = "rose-pine" if self.dark else "rose-pine-dawn"
        self.push_screen(Main())


def run() -> None:
    ScientiaCore().run()
