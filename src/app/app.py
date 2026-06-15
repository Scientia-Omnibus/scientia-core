from argparse import ArgumentParser, Namespace

from textual import __version__ as scientia_version
from textual.app import App

from src import __version__
from src.data import load_config
from src.screens import Main


class ScientiaCore(App[None]):
    TITLE = "Scientia Omnibus"
    ENABLE_COMMAND_PALETTE = False

    def __init__(self, cli_args: Namespace) -> None:
        super().__init__()
        self._args = cli_args
        self.dark = not load_config().light_mode

    def on_mount(self) -> None:
        self.push_screen(Main(" ".join(self._args.file) if self._args.file else None))


def get_args() -> Namespace:

    parser = ArgumentParser(
        prog="Scientia Core",
        description="Scientia -- light-weight app with a lot of knowledge.",
    )

    parser.add_argument(
        "file",
        nargs="*",
        help="A Markdown file to view.",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information.",
        action="version",
        version=f"%(prog)s {__version__} (Scientia v{scientia_version})",
    )
    return parser.parse_args()


def run() -> None:
    ScientiaCore(get_args()).run()
