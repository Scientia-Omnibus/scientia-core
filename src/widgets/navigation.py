from __future__ import annotations

import asyncio
from pathlib import Path

import git
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var
from textual.widgets import TabbedContent, Tabs
from typing_extensions import Self

from data import load_config, save_config
from data.data_directory import data_directory
from dialogs.directory_picker import DirectoryPicker
from dialogs.error import ErrorDialog
from dialogs.knowledge_sync import KnowledgeSync
from dialogs.progress_screen import ProgressScreen
from widgets.navigation_panes.bookmarks import Bookmarks
from widgets.navigation_panes.history import History
from widgets.navigation_panes.local_files import LocalFiles
from widgets.navigation_panes.navigation_pane import NavigationPane
from widgets.navigation_panes.table_of_contents import TableOfContents
from widgets.omnibox import Omnibox


class Navigation(Vertical, can_focus=True, can_focus_children=True):
    DEFAULT_CSS = """
    Navigation {
        width: 35%;
        background: $panel;
        display: block;
        dock: left;
    }

    Navigation.hidden {
        display: none;
    }

    TabbedContent {
        height: 100% !important;
    }

    ContentSwitcher {
        height: 1fr !important;
    }
    """

    BINDINGS = [
        Binding("comma,a,ctrl+left,shift+left,h", "previous_tab", "", show=False),
        Binding("full_stop,d,ctrl+right,shift+right,l", "next_tab", "", show=False),
        Binding("\\", "toggle_dock", "Dock left/right"),
    ]

    popped_out: var[bool] = var(False)
    docked_left: var[bool] = var(True)

    def compose(self) -> ComposeResult:
        self.popped_out = True
        self._contents = TableOfContents()
        self._local_files = LocalFiles()
        self._bookmarks = Bookmarks()
        self._history = History()
        with TabbedContent() as tabs:
            self._tabs = tabs
            yield self._contents
            yield self._local_files
            yield self._bookmarks
            yield self._history

    def on_mount(self) -> None:
        self.docked_left = load_config().navigation_left

    class Hidden(Message):
        pass

    def watch_popped_out(self) -> None:
        self.set_class(not self.popped_out, "hidden")
        if not self.popped_out:
            self.post_message(self.Hidden())

    def toggle(self) -> None:
        self.popped_out = not self.popped_out

    def watch_docked_left(self) -> None:
        self.styles.dock = "left" if self.docked_left else "right"

    @property
    def table_of_contents(self) -> TableOfContents:
        return self._contents

    @property
    def local_files(self) -> LocalFiles:
        return self._local_files

    @property
    def bookmarks(self) -> Bookmarks:
        return self._bookmarks

    @property
    def history(self) -> History:
        return self._history

    def jump_to_local_files(self, target: Path | None = None) -> Self:
        """Switch to and focus the local files pane.

        Returns:
            Self.
        """
        if (
            self.popped_out
            and target is None
            and self.query_one(Tabs).active == self._local_files.id
        ):
            self.popped_out = False
        else:
            self.popped_out = True
            if target is not None:
                self._local_files.chdir(target)
            self._local_files.activate().set_focus_within()
        return self

    def jump_to_bookmarks(self) -> Self:
        """Switch to and focus the bookmarks pane.

        Returns:
            Self.
        """
        if self.popped_out and self.query_one(Tabs).active == self._bookmarks.id:
            self.popped_out = False
        else:
            self.popped_out = True
            self._bookmarks.activate().set_focus_within()
        return self

    def jump_to_history(self) -> Self:
        """Switch to and focus the history pane.

        Returns:
            Self.
        """
        if self.popped_out and self.query_one(Tabs).active == self._history.id:
            self.popped_out = False
        else:
            self.popped_out = True
            self._history.activate().set_focus_within()
        return self

    def jump_to_contents(self) -> Self:
        """Switch to and focus the table of contents pane.

        Returns:
            Self.
        """
        if self.popped_out and self.query_one(Tabs).active == self._contents.id:
            self.popped_out = False
        else:
            self.popped_out = True
            self._contents.activate().set_focus_within()
        return self

    def action_previous_tab(self) -> None:
        """Switch to the previous tab in the navigation pane."""
        self.query_one(Tabs).action_previous_tab()
        self.focus_tab()

    def action_next_tab(self) -> None:
        """Switch to the next tab in the navigation pane."""
        self.query_one(Tabs).action_next_tab()
        self.focus_tab()

    def action_toggle_dock(self) -> None:
        """Toggle the dock side for the navigation."""
        config = load_config()
        config.navigation_left = not config.navigation_left
        save_config(config)
        self.docked_left = config.navigation_left

    def focus_tab(self) -> None:
        """Focus the currently active tab."""
        if active := self.query_one(Tabs).active:
            self.query_one(
                f"NavigationPane#{active}", NavigationPane
            ).set_focus_within()

    def change_knowledge_dir(self) -> None:
        self.app.push_screen(DirectoryPicker(), self._on_dir_selected)

    def update_knowledge_base(self) -> None:
        self.app.push_screen(KnowledgeSync(), self._sync_knowledge_base)

    def _on_dir_selected(self, target: Path | None) -> None:
        if target:
            self.post_message(Omnibox.LocalChdirCommand(target))

    async def _sync_knowledge_base(self, repo_name: str) -> None:
        self.app.push_screen(ProgressScreen("Syncing knowledge base..."))
        repo_path = f"https://github.com/Scientia-Omnibus/{repo_name}"
        target_path = data_directory() / repo_name
        try:
            if target_path.exists():
                repo = git.Repo(target_path)
                await asyncio.to_thread(repo.remotes.origin.fetch, "main")
                repo.git.reset("--hard", "origin/main")
                repo.git.clean("-fd")
            else:
                await asyncio.to_thread(git.Repo.clone_from, repo_path, target_path)
            self.app.pop_screen()
            self.post_message(Omnibox.LocalChdirCommand(data_directory()))
        except Exception:
            self.app.pop_screen()
            self.app.push_screen(
                ErrorDialog(
                    "Oops...",
                    "Error while syncing repositories.",
                )
            )
