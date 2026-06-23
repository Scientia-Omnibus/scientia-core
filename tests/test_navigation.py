from __future__ import annotations

from textual.widgets import TabbedContent

from widgets.navigation import Navigation


async def test_navigation_initial_state() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        assert nav.popped_out is True
        assert nav.docked_left is True


async def test_navigation_toggle() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        assert nav.popped_out is True
        assert not nav.has_class("hidden")
        nav.toggle()
        assert nav.popped_out is False
        assert nav.has_class("hidden")
        nav.toggle()
        assert nav.popped_out is True
        assert not nav.has_class("hidden")


async def test_navigation_tabs_present() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        tabs = nav.query_one(TabbedContent)
        assert tabs.tab_count == 4


async def test_navigation_jump_to_contents() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        nav.jump_to_contents()
        tabs = nav.query_one(TabbedContent)
        assert tabs.active == nav.table_of_contents.id


async def test_navigation_jump_to_local_files() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        nav.jump_to_local_files()
        tabs = nav.query_one(TabbedContent)
        assert tabs.active == nav.local_files.id


async def test_navigation_jump_to_bookmarks() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        nav.jump_to_bookmarks()
        tabs = nav.query_one(TabbedContent)
        assert tabs.active == nav.bookmarks.id


async def test_navigation_jump_to_history() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

    async with TestApp().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        nav.jump_to_history()
        tabs = nav.query_one(TabbedContent)
        assert tabs.active == nav.history.id


async def test_navigation_hidden_message() -> None:
    hidden_called = False

    class TestApp(Navigation):
        pass

    from textual.app import App, ComposeResult

    class TestContainer(App):
        def compose(self) -> ComposeResult:
            yield Navigation()

        def on_navigation_hidden(self) -> None:
            nonlocal hidden_called
            hidden_called = True

    async with TestContainer().run_test() as pilot:
        nav = pilot.app.query_one(Navigation)
        nav.toggle()
        await pilot.pause()
        assert hidden_called
