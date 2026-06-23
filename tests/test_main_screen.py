from __future__ import annotations

from textual.widgets import Footer, ListView, Markdown

from dialogs import HelpDialog, InformationDialog, InputDialog
from screens.main import Main
from widgets import Omnibox, Viewer


async def test_main_screen_compose() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        assert isinstance(main, Main)
        assert main.query_one(Omnibox) is not None
        assert main.query_one(Viewer) is not None
        assert main.query_one(Footer) is not None
        results = main.query_one("#omnibox-results", ListView)
        assert results is not None


async def test_main_screen_omnibox_focus_on_slash() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        await pilot.press("/")
        await pilot.pause()
        assert main.query_one(Omnibox).has_focus


async def test_main_screen_omnibox_focus_on_colon() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        await pilot.press(":")
        await pilot.pause()
        assert main.query_one(Omnibox).has_focus


async def test_main_screen_escape_clears_omnibox() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        omni = main.query_one(Omnibox)
        omni.focus()
        omni.value = "search text"
        await pilot.press("escape")
        await pilot.pause()
        assert omni.value == ""


async def test_main_screen_help_dialog_opens() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("f1")
        await pilot.pause()
        assert isinstance(pilot.app.screen, HelpDialog)


async def test_main_screen_about_dialog_opens() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("f2")
        await pilot.pause()
        assert isinstance(pilot.app.screen, InformationDialog)


async def test_main_screen_bookmark_this_opens_input() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        viewer = main.query_one(Viewer)
        from pathlib import Path

        viewer.history.remember(Path("/tmp/test.md"))
        viewer.viewing_location = True
        await pilot.press("ctrl+d")
        await pilot.pause()
        assert isinstance(pilot.app.screen, InputDialog)


async def test_main_screen_viewer_has_placeholder() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        main = pilot.app.screen
        viewer = main.query_one(Viewer)
        md = viewer.query_one(Markdown)
        assert md is not None


async def test_main_screen_back_forward_bindings() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("ctrl+left")
        await pilot.pause()
        await pilot.press("ctrl+right")
        await pilot.pause()


async def test_main_screen_reload_binding() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(Main())

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("ctrl+r")
        await pilot.pause()
