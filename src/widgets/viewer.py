from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Callable

from markdown_it import MarkdownIt
from mdit_py_plugins import front_matter
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.widgets import Markdown
from typing_extensions import Final

from app import __version__
from dialogs import ErrorDialog

APPLICATION_TITLE = "Scientia Omnibus"

PLACEHOLDER = f"""\
# Welcome to {APPLICATION_TITLE}  `v{__version__}`

---

> A quiet place for the things you save and read later.

---

### 📦 Store

Everything lives in **Markdown files** — downloaded once, stored locally,
always available. No internet required once you have what you need.

### 🧭 Navigate

The omnibox at the top is the main way to get around. Type **`/`** or **`:`**
to focus it, search by title, or run a command.

The sidebar has four tabs: **Contents**, **Local files**, **Bookmarks**, and **History**.

### 💻 About

It is a small program — **under 10 MB** — and runs on almost anything.
Old laptops, cheap single-board computers, you name it.

---

> **Tip:** Press **`F1`** at any time to see all available commands.
"""


class History:
    MAXIMUM_HISTORY_LENGTH: Final[int] = 256

    def __init__(self, history: list[Path] | None = None) -> None:
        self._history: deque[Path] = deque(
            history or [], maxlen=self.MAXIMUM_HISTORY_LENGTH
        )
        self._current: int = max(len(self._history) - 1, 0)

    @property
    def location(self) -> Path | None:
        try:
            return self._history[self._current]
        except IndexError:
            return None

    @property
    def current(self) -> int | None:
        return None if self.location is None else self._current

    @property
    def locations(self) -> list[Path]:
        return list(self._history)

    def remember(self, location: Path) -> None:
        self._history.append(location)
        self._current = len(self._history) - 1

    def back(self) -> bool:
        if self._current:
            self._current -= 1
            return True
        return False

    def forward(self) -> bool:
        if self._current < len(self._history) - 1:
            self._current += 1
            return True
        return False

    def __delitem__(self, index: int) -> None:
        del self._history[index]
        self._current = max(len(self._history) - 1, self._current)


class Viewer(VerticalScroll, can_focus=True, can_focus_children=True):
    DEFAULT_CSS = """
    Viewer {
        width: 1fr;
        scrollbar-gutter: stable;
    }
    """

    BINDINGS = [
        Binding("w,k", "scroll_up", "", show=False),
        Binding("s,j", "scroll_down", "", show=False),
        Binding("space", "page_down", "", show=False),
        Binding("b", "page_up", "", show=False),
    ]

    history: var[History] = var(History)
    viewing_location: var[bool] = var(False)

    class ViewerMessage(Message):
        def __init__(self, viewer: Viewer) -> None:
            super().__init__()
            self.viewer: Viewer = viewer

    class LocationChanged(ViewerMessage):
        pass

    class HistoryUpdated(ViewerMessage):
        pass

    def compose(self) -> ComposeResult:
        yield Markdown(
            PLACEHOLDER,
            parser_factory=lambda: MarkdownIt("gfm-like").use(
                front_matter.front_matter_plugin
            ),
        )

    @property
    def document(self) -> Markdown:
        return self.query_one(Markdown)

    @property
    def location(self) -> Path | None:
        return self.history.location if self.viewing_location else None

    def scroll_to_block(self, block_id: str) -> None:
        self.scroll_to_widget(self.document.query_one(f"#{block_id}"), top=True)

    def _post_load(self, location: Path, remember: bool = True) -> None:
        self.scroll_home(animate=False)
        self.viewing_location = True
        if remember:
            self.history.remember(location)
            self.post_message(self.HistoryUpdated(self))
        self.post_message(self.LocationChanged(self))

    @work(exclusive=True)
    async def _local_load(self, location: Path, remember: bool = True) -> None:
        try:
            await self.document.load(location)
        except OSError as error:
            self.app.push_screen(
                ErrorDialog(
                    "Error loading local document",
                    f"{location}\n\n{error}.",
                )
            )
        else:
            self._post_load(location, remember)

    def visit(self, location: Path, remember: bool = True) -> None:
        self._local_load(location.expanduser().resolve(), remember)

    def reload(self) -> None:
        if self.location is not None:
            self.visit(self.location, False)

    def show(self, content: str) -> None:
        self.viewing_location = False
        self.document.update(content)
        self.scroll_home(animate=False)

    def _jump(self, direction: Callable[[], bool]) -> None:
        if direction():
            if self.history.location is not None:
                self.visit(self.history.location, remember=False)

    def back(self) -> None:
        self._jump(self.history.back)

    def forward(self) -> None:
        self._jump(self.history.forward)

    def load_history(self, history: list[Path]) -> None:
        self.history = History(history)
        self.post_message(self.HistoryUpdated(self))

    def delete_history(self, history_id: int) -> None:
        try:
            del self.history[history_id]
        except IndexError:
            pass
        else:
            self.post_message(self.HistoryUpdated(self))

    def clear_history(self) -> None:
        self.load_history([])
