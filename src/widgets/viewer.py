from __future__ import annotations

import re
from collections import deque
from pathlib import Path
from typing import Callable

from markdown_it import MarkdownIt
from mdit_py_plugins import front_matter
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.containers import VerticalScroll
from textual.content import Span
from textual.message import Message
from textual.reactive import var
from textual.style import Style
from textual.widgets import Markdown
from typing_extensions import Final

from app import __version__
from dialogs.error import ErrorDialog
from widgets.find_bar import FindBar
from widgets.helpers import (
    _build_line_offsets,
    _find_next,
    _find_prev,
    _text_offset_to_location,
)

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
        height: 1fr;
        min-height: 0;
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._source_text: str = PLACEHOLDER
        self._line_offsets: list[int] = _build_line_offsets(PLACEHOLDER)
        self._find_offset: int | None = None
        self._original_contents: dict = {}

    class ViewerMessage(Message):
        def __init__(self, viewer: Viewer) -> None:
            super().__init__()
            self.viewer: Viewer = viewer

    class LocationChanged(ViewerMessage):
        pass

    class HistoryUpdated(ViewerMessage):
        pass

    def compose(self) -> ComposeResult:
        yield FindBar()
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
    def find_bar(self) -> FindBar:
        return self.query_one(FindBar)

    @property
    def location(self) -> Path | None:
        return self.history.location if self.viewing_location else None

    def show_find(self) -> None:
        self._find_offset = None
        self.find_bar.show_find()

    def scroll_to_block(self, block_id: str) -> None:
        self.scroll_to_widget(self.document.query_one(f"#{block_id}"), top=True)

    def _set_source_text(self, text: str) -> None:
        self._source_text = text
        self._line_offsets = _build_line_offsets(text)
        self._find_offset = None
        self._clear_highlights()

    def _clear_highlights(self) -> None:
        for block, original in self._original_contents.items():
            try:
                block.set_content(original)
            except Exception:
                pass
        self._original_contents.clear()

    def _highlight_matches(
        self, query: str, case_sensitive: bool, match_index: int | None = None
    ) -> None:
        self._clear_highlights()
        if not query or match_index is None:
            return

        hl = Style(background=Color(196, 167, 231))
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(query), flags)

        count = 0
        for block in self.document.query("MarkdownBlock"):
            try:
                content = block._content
            except AttributeError:
                continue
            for match in pattern.finditer(content.plain):
                count += 1
                if count == match_index:
                    start, end = match.span()
                    highlighted = content.add_spans([Span(start, end, hl)])
                    self._original_contents[block] = content
                    block.set_content(highlighted)
                    self.document.refresh()
                    return

    def _match_status(
        self, query: str, case_sensitive: bool, current_start: int
    ) -> tuple[int, int]:
        index = 0
        total = 0
        pos = 0
        while True:
            start, end = _find_next(self._source_text, query, pos, case_sensitive)
            if start < 0 or start < pos:
                break
            total += 1
            if start == current_start:
                index = total
            pos = end
        return index, total

    def scroll_to_offset(self, offset: int) -> None:
        row, _ = _text_offset_to_location(self._source_text, offset, self._line_offsets)
        blocks = list(self.document.query("MarkdownBlock"))
        if blocks:
            line_count = self._source_text.count("\n") + 1
            block_index = min(
                int(row / max(line_count, 1) * len(blocks)), len(blocks) - 1
            )
            self.scroll_to_widget(blocks[block_index], top=True)
            return
        line_count = max(self._source_text.count("\n"), 1)
        self.scroll_y = int((row / line_count) * self.max_scroll_y)

    @on(FindBar.FindNext)
    def on_find_bar_find_next(self, event: FindBar.FindNext) -> None:
        if not event.query:
            return

        cursor = self._find_offset if self._find_offset is not None else 0
        start, end = _find_next(
            self._source_text, event.query, cursor, event.case_sensitive
        )
        if start < 0:
            self._find_offset = None
            self._clear_highlights()
            self.find_bar.set_status("No matches")
            return

        self._find_offset = end
        self.scroll_to_offset(start)
        index, total = self._match_status(event.query, event.case_sensitive, start)
        self._highlight_matches(event.query, event.case_sensitive, match_index=index)
        self.find_bar.set_status(f"{index} / {total}")

    @on(FindBar.FindPrevious)
    def on_find_bar_find_previous(self, event: FindBar.FindPrevious) -> None:
        if not event.query:
            return

        cursor = (
            self._find_offset
            if self._find_offset is not None
            else len(self._source_text)
        )
        start, end = _find_prev(
            self._source_text, event.query, cursor, event.case_sensitive
        )
        if start < 0:
            self._find_offset = None
            self._clear_highlights()
            self.find_bar.set_status("No matches")
            return

        self._find_offset = start
        self.scroll_to_offset(start)
        index, total = self._match_status(event.query, event.case_sensitive, start)
        self._highlight_matches(event.query, event.case_sensitive, match_index=index)
        self.find_bar.set_status(f"{index} / {total}")

    @on(FindBar.Closed)
    def on_find_bar_closed(self) -> None:
        self._find_offset = None
        self._clear_highlights()
        self.focus()

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
            self._set_source_text(location.read_text(encoding="utf-8"))
            self._post_load(location, remember)

    def visit(self, location: Path, remember: bool = True) -> None:
        self._local_load(location.expanduser().resolve(), remember)

    def reload(self) -> None:
        if self.location is not None:
            self.visit(self.location, False)

    def show(self, content: str) -> None:
        self.viewing_location = False
        self._set_source_text(content)
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
