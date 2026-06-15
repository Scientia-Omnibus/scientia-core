import webbrowser

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Markdown
from typing_extensions import Final

from src import __version__

HELP: Final[str] = f"""\
# Scientia Omnibus v{__version__} Help

Welcome to Scientia Omnibus Help!

## Navigation keys

| Key | Command |
| -- | -- |
| `/` | Focus the address bar |
| `Escape` | Return to address bar / clear address bar / quit |
| `Ctrl+n` | Show/hide the navigation |
| `Ctrl+b` | Show the bookmarks |
| `Ctrl+l` | Show the local file browser |
| `Ctrl+t` | Show the table of contents |
| `Ctrl+y` | Show the history |
| `Ctrl+left` | Go backward in history |
| `Ctrl+right` | Go forward in history |

## General keys

| Key | Command |
| -- | -- |
| `Ctrl+d` | Add the current document to the bookmarks |
| `Ctrl+r` | Reload the current document |
| `Ctrl+q` | Quit the application |
| `F1` | This help |
| `F2` | Details about Scientia Omnibus |
| `F10` | Toggle dark/light theme |

## Commands

Press `/` or click the address bar, then enter any of the following commands:

| Command | Aliases | Arguments | Command |
| -- | -- | -- | -- |
| `about` | `a` | | Show details about the application |
| `bookmarks` | `b`, `bm` | | Show the bookmarks list |
| `chdir` | `cd` | `<dir>` | Switch the local file browser to a new directory |
| `contents` | `c`, `toc` | | Show the table of contents for the document |
| `help` | `?` | | Show this document |
| `history` | `h` | | Show the history |
| `local` | `l` | | Show the local file browser |
| `quit` | `q` | | Quit the viewer |
"""


class HelpDialog(ModalScreen[None]):
    DEFAULT_CSS = """
    HelpDialog {
        align: center middle;
    }

    HelpDialog > Vertical {
        border: thick $primary 50%;
        width: 80%;
        height: 80%;
        background: $boost;
    }

    HelpDialog > Vertical > VerticalScroll {
        height: 1fr;
        margin: 1 2;
    }

    HelpDialog > Vertical > Center {
        padding: 1;
        height: auto;
    }
    """

    BINDINGS = [
        Binding("escape,f1", "dismiss(None)", "", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Vertical():
            with VerticalScroll():
                yield Markdown(HELP)
            with Center():
                yield Button("Close", variant="primary")

    def on_mount(self) -> None:
        self.query_one(Markdown).can_focus_children = False
        self.query_one("Vertical > VerticalScroll").focus()

    def on_button_pressed(self) -> None:
        self.dismiss(None)

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        webbrowser.open(event.href)
