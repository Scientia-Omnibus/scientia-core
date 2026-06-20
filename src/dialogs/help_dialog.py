import webbrowser

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Markdown
from typing_extensions import Final

from app import __version__

HELP: Final[str] = f"""\
# Scientia Omnibus v{__version__} Help

Scientia Omnibus — a terminal program for viewing your knowledge base.

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
| `Ctrl+G` | Download or update knowledge base repositories |
| `Ctrl+O` | Change the search directory |
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

## Search

As you type in the omnibox, fuzzy search automatically scans the knowledge directory
for matching `.md` files. Results appear in a dropdown list below the omnibox.

- `Down` arrow — move focus to the results list.
- `Up` arrow (at the top of results) — return focus to the omnibox.
- `Enter` — open the selected file in the viewer.
- `Escape` — close the results dropdown.

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

## Knowledge Base Sync

`Ctrl+G` opens a dialog to download or update knowledge repositories. Four repositories are available:

- **humanities-sciences**
- **social-sciences**
- **natural-sciences**
- **formal-sciences**

Select a repository and press `OK`. If the repository already exists locally, it will be
force-synced — any local changes are overwritten with the remote version. If it does not
exist, it will be cloned from GitHub (`github.com/Scientia-Omnibus`).

After syncing, the file tree navigates to the downloaded repository so you can browse
its contents immediately.
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
