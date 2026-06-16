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

Scientia Omnibus — a terminal program for viewing your education storage.

## Interface

The application consists of three main zones:

- **Omnibox** (top bar) — a command line, like a browser address bar.
- **Navigation** (sidebar) — four tabs: Contents, Local, Bookmarks, History.
- **Viewer** (main area) — displays documents.

The sidebar can be hidden/shown (`Ctrl+N`), tabs can be switched,
or the panel can be moved to the opposite side (`\\`).

## Global Keys

| Key | Action |
| -- | -- |
| `/` or `:` | Focus on omnibox (command line) |
| `Escape` | Return to omnibox / clear omnibox / exit |
| `Ctrl+N` | Show/hide navigation sidebar |
| `Ctrl+B` | Show bookmarks |
| `Ctrl+L` | Show local files |
| `Ctrl+T` | Show document table of contents |
| `Ctrl+Y` | Show history |
| `Ctrl+Left` | Go back in viewing history |
| `Ctrl+Right` | Go forward in viewing history |
| `Ctrl+D` | Add current document to bookmarks |
| `Ctrl+R` | Reload current document |
| `Ctrl+Q` | Quit application |
| `F1` | This help |
| `F2` | About |
| `F10` | Toggle dark/light theme |

## Navigation Panel

| Key | Action |
| -- | -- |
| `,` / `a` / `h` / `Ctrl+Left` / `Shift+Left` | Previous tab |
| `.` / `d` / `l` / `Ctrl+Right` / `Shift+Right` | Next tab |
| `\\` | Move panel left/right |

## Document Viewer

When focus is in the viewer:

| Key | Action |
| -- | -- |
| `w` / `k` | Scroll up |
| `s` / `j` | Scroll down |
| `Space` | Page down |
| `b` | Page up |

## Bookmarks

| Key | Action |
| -- | -- |
| `Delete` | Delete bookmark |
| `r` | Rename bookmark |

## History

| Key | Action |
| -- | -- |
| `Delete` | Delete history entry |
| `Backspace` | Clear entire history |

## Commands

Press `/` or click the omnibox, then type one of the commands:

| Command | Aliases | Description |
| -- | -- | -- |
| `about` | `a` | Show application information |
| `bookmarks` | `b`, `bm` | Show bookmarks list |
| `contents` | `c`, `toc` | Show document table of contents |
| `help` | `?` | Show this help |
| `history` | `h` | Show history |
| `local` | `l` | Show local files |
| `quit` | `q` | Quit the program |

You can also simply type a path to a `.md` file to open it.
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
