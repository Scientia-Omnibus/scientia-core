from __future__ import annotations

from pathlib import Path

from textual.message import Message
from textual.widgets import Input


class Omnibox(Input):
    DEFAULT_CSS = """
    Omnibox {
        dock: top;
        padding: 0;
        height: 3;
    }

    Omnibox .input--placeholder {
        color: $text 50%;
    }
    """

    def on_mount(self) -> None:
        self.placeholder = "Search file, or enter a command... (type `help` for more)"

    _ALIASES: dict[str, str] = {
        "a": "about",
        "b": "bookmarks",
        "bm": "bookmarks",
        "c": "contents",
        "cd": "chdir",
        "h": "history",
        "l": "local",
        "toc": "contents",
        "q": "quit",
        "?": "help",
    }

    @staticmethod
    def _split_command(value: str) -> list[str]:
        command = value.split(None, 1)
        return [*command, ""] if len(command) == 1 else command

    def _is_command(self, value: str) -> bool:
        command, *_ = self._split_command(value)
        return (
            getattr(self, f"command_{self._ALIASES.get(command, command)}", None)
            is not None
        )

    def _execute_command(self, command: str) -> None:
        command, arguments = self._split_command(command)
        getattr(self, f"command_{self._ALIASES.get(command, command)}")(
            arguments.strip()
        )

    class LocalViewCommand(Message):
        def __init__(self, path: Path) -> None:
            super().__init__()
            self.path = path

    class LocalChdirCommand(Message):
        def __init__(self, target: Path) -> None:
            super().__init__()
            self.target = target

    def on_input_submitted(self, event: Input.Submitted) -> None:
        submitted = self.value.strip()
        self.value = ""
        if self._is_command(command := submitted.lower()):
            self._execute_command(command)
        event.stop()

    class ContentsCommand(Message):
        pass

    def command_contents(self, _: str) -> None:
        self.post_message(self.ContentsCommand())

    class LocalFilesCommand(Message):
        pass

    def command_local(self, _: str) -> None:
        self.post_message(self.LocalFilesCommand())

    class BookmarksCommand(Message):
        pass

    def command_bookmarks(self, _: str) -> None:
        self.post_message(self.BookmarksCommand())

    class QuitCommand(Message):
        pass

    def command_quit(self, _: str) -> None:
        self.post_message(self.QuitCommand())

    class HistoryCommand(Message):
        pass

    def command_history(self, _: str) -> None:
        self.post_message(self.HistoryCommand())

    class AboutCommand(Message):
        pass

    def command_about(self, _: str) -> None:
        self.post_message(self.AboutCommand())

    class HelpCommand(Message):
        pass

    def command_help(self, _: str) -> None:
        self.post_message(self.HelpCommand())
