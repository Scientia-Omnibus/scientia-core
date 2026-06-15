from __future__ import annotations

from functools import partial
from pathlib import Path
from webbrowser import open as open_url

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import Paste
from textual.screen import Screen
from textual.widgets import Footer, Markdown

from src import __version__
from src.data import load_config, load_history, save_config, save_history
from src.dialogs import ErrorDialog, HelpDialog, InformationDialog, InputDialog
from src.utility import maybe_markdown
from src.widgets import Navigation, Omnibox, Viewer
from src.widgets.navigation_panes import Bookmarks, History, LocalFiles


class Main(Screen[None]):
    DEFAULT_CSS = """
    .focusable {
        border: blank;
    }

    .focusable:focus {
        border: heavy $accent !important;
    }


    Screen Tabs {
        border: blank;
        height: 5;
    }

    Screen Tabs:focus {
        border: heavy $accent !important;
        height: 5;
    }

    Screen TabbedContent TabPane {
        padding: 0 1;
        border: blank;
    }

    Screen TabbedContent TabPane:focus-within {
        border: heavy $accent !important;
    }
    """

    BINDINGS = [
        Binding("/,:", "omnibox", "Omnibox", show=False),
        Binding("ctrl+b", "bookmarks", "", show=False),
        Binding("ctrl+d", "bookmark_this", "", show=False),
        Binding("ctrl+l", "local_files", "", show=False),
        Binding("ctrl+left", "backward", "", show=False),
        Binding("ctrl+right", "forward", "", show=False),
        Binding("ctrl+r", "reload", "", show=False),
        Binding("ctrl+t", "table_of_contents", "", show=False),
        Binding("ctrl+y", "history", "", show=False),
        Binding("escape", "escape", "", show=False),
        Binding("f1", "help", "Help"),
        Binding("f2", "about", "About"),
        Binding("ctrl+n", "navigation", "Navigation"),
        Binding("ctrl+q", "app.quit", "Quit"),
        Binding("f10", "toggle_theme", "", show=False),
    ]

    def __init__(self, initial_location: str | None = None) -> None:
        super().__init__()
        self._initial_location = initial_location

    def compose(self) -> ComposeResult:
        yield Omnibox(classes="focusable")
        with Horizontal():
            yield Navigation()
            yield Viewer(classes="focusable")
        yield Footer()

    def visit(self, location: Path, remember: bool = True) -> None:
        if maybe_markdown(location):
            self.query_one(Viewer).visit(location, remember)
        elif location.exists():
            open_url(f"file:///{location.absolute()}")
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Does not exist",
                    f"Unable to open {location} because it does not exist.",
                )
            )

    async def on_mount(self) -> None:
        self.query_one(Viewer).document.can_focus_children = False

        if history := load_history():
            self.query_one(Viewer).load_history(history)

        if self._initial_location is None and history:
            self.query_one(Viewer).visit(history[-1], remember=False)
            self.query_one(Omnibox).value = str(history[-1])
        elif self._initial_location is not None:
            (omnibox := self.query_one(Omnibox)).value = self._initial_location
            await omnibox.action_submit()

    def on_navigation_hidden(self) -> None:
        self.query_one(Viewer).focus()

    def on_omnibox_local_view_command(self, event: Omnibox.LocalViewCommand) -> None:
        self.visit(event.path)

    def on_omnibox_contents_command(self) -> None:
        self.action_table_of_contents()

    def on_omnibox_local_files_command(self) -> None:
        self.action_local_files()

    def on_omnibox_bookmarks_command(self) -> None:
        self.action_bookmarks()

    def on_omnibox_local_chdir_command(self, event: Omnibox.LocalChdirCommand) -> None:
        if not event.target.exists():
            self.app.push_screen(
                ErrorDialog("No such directory", f"{event.target} does not exist.")
            )
        elif not event.target.is_dir():
            self.app.push_screen(
                ErrorDialog("Not a directory", f"{event.target} is not a directory.")
            )
        else:
            self.query_one(Navigation).jump_to_local_files(event.target)

    def on_omnibox_history_command(self) -> None:
        self.action_history()

    def on_omnibox_about_command(self) -> None:
        self.action_about()

    def on_omnibox_help_command(self) -> None:
        self.action_help()

    def on_omnibox_quit_command(self) -> None:
        self.app.exit()

    def on_local_files_goto(self, event: LocalFiles.Goto) -> None:
        self.visit(event.location)

    def on_history_goto(self, event: History.Goto) -> None:
        self.visit(
            event.location, remember=event.location != self.query_one(Viewer).location
        )

    def on_history_delete(self, event: History.Delete) -> None:
        self.query_one(Viewer).delete_history(event.history_id)

    def on_history_clear(self) -> None:
        self.query_one(Viewer).clear_history()

    def on_bookmarks_goto(self, event: Bookmarks.Goto) -> None:
        self.visit(event.bookmark.location)

    def on_viewer_location_changed(self, event: Viewer.LocationChanged) -> None:
        self.query_one(Omnibox).visiting = (
            str(event.viewer.location) if event.viewer.location is not None else ""
        )
        self.query_one(Viewer).focus()

    def on_viewer_history_updated(self, event: Viewer.HistoryUpdated) -> None:
        self.query_one(Navigation).history.update_from(event.viewer.history.locations)
        save_history(event.viewer.history.locations)

    def on_markdown_table_of_contents_updated(
        self, event: Markdown.TableOfContentsUpdated
    ) -> None:
        self.query_one(Navigation).table_of_contents.on_table_of_contents_updated(event)

    def on_markdown_table_of_contents_selected(
        self, event: Markdown.TableOfContentsSelected
    ) -> None:
        self.query_one(Viewer).scroll_to_block(event.block_id)

    def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        current_location = self.query_one(Viewer).location
        if (local_file := Path(event.href)).exists():
            self.visit(local_file)
        elif (
            isinstance(current_location, Path)
            and (local_file := (current_location.parent / Path(event.href)))
            .absolute()
            .exists()
        ):
            self.visit(local_file)
        elif event.href.startswith("#") and event.markdown.goto_anchor(event.href[1:]):
            pass
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Unable to handle link",
                    f"Unable to work out how to handle this link:\n\n{event.href}",
                )
            )

    def on_paste(self, event: Paste) -> None:
        if (candidate_file := Path(event.text)).exists():
            self.visit(candidate_file)

    def action_navigation(self) -> None:
        self.query_one(Navigation).toggle()

    def action_escape(self) -> None:
        if (omnibox := self.query_one(Omnibox)).has_focus:
            if omnibox.value:
                omnibox.value = ""
            else:
                self.app.exit()
        else:
            if self.query("Navigation:focus-within"):
                self.query_one(Navigation).popped_out = False
            omnibox.focus()

    def action_omnibox(self) -> None:
        self.query_one(Omnibox).focus()

    def action_table_of_contents(self) -> None:
        self.query_one(Navigation).jump_to_contents()

    def action_local_files(self) -> None:
        self.query_one(Navigation).jump_to_local_files()

    def action_bookmarks(self) -> None:
        self.query_one(Navigation).jump_to_bookmarks()

    def action_history(self) -> None:
        self.query_one(Navigation).jump_to_history()

    def action_backward(self) -> None:
        self.query_one(Viewer).back()

    def action_forward(self) -> None:
        self.query_one(Viewer).forward()

    def action_help(self) -> None:
        self.app.push_screen(HelpDialog())

    def action_about(self) -> None:
        self.app.push_screen(
            InformationDialog(
                f"Scientia Omnibus [b dim]v{__version__}",
                "https://github.com/Scientia-Omnibus",
            )
        )

    def add_bookmark(self, location: Path, bookmark: str) -> None:
        self.query_one(Navigation).bookmarks.add_bookmark(bookmark, location)

    def action_bookmark_this(self) -> None:
        location = self.query_one(Viewer).location
        if not isinstance(location, Path):
            self.app.push_screen(
                ErrorDialog(
                    "Not a bookmarkable location",
                    "The current view can't be bookmarked.",
                )
            )
            return

        title = location.name

        self.app.push_screen(
            InputDialog("Bookmark title:", title),
            partial(self.add_bookmark, location),
        )

    def action_toggle_theme(self) -> None:
        config = load_config()
        config.light_mode = not config.light_mode
        save_config(config)
        self.app.dark = not config.light_mode

    def action_reload(self) -> None:
        self.query_one(Viewer).reload()
