from __future__ import annotations

from widgets.omnibox import Omnibox


async def test_omnibox_placeholder() -> None:
    from textual.app import App

    class TestApp(App):
        def compose(self):
            yield Omnibox()

    async with TestApp().run_test() as pilot:
        omnibox = pilot.app.query_one(Omnibox)
        assert omnibox.placeholder


async def test_omnibox_is_command() -> None:
    omnibox = Omnibox()
    assert omnibox._is_command("help")
    assert omnibox._is_command("about")
    assert omnibox._is_command("bookmarks")
    assert omnibox._is_command("history")
    assert omnibox._is_command("contents")
    assert omnibox._is_command("local")
    assert omnibox._is_command("quit")
    assert not omnibox._is_command("foobar")
    assert not omnibox._is_command("")


async def test_omnibox_aliases() -> None:
    omnibox = Omnibox()
    assert omnibox._is_command("?")
    assert omnibox._is_command("a")
    assert omnibox._is_command("b")
    assert omnibox._is_command("bm")
    assert omnibox._is_command("c")
    assert omnibox._is_command("h")
    assert omnibox._is_command("l")
    assert omnibox._is_command("toc")
    assert omnibox._is_command("q")


async def test_omnibox_split_command() -> None:
    omnibox = Omnibox()
    assert omnibox._split_command("help") == ["help", ""]
    assert omnibox._split_command("local /some/path") == ["local", "/some/path"]
    assert omnibox._split_command("") == ["", ""]


async def test_omnibox_key_escape_clears_value() -> None:
    from textual.app import App

    class TestApp(App):
        def compose(self):
            yield Omnibox(id="omni")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "hello"
        await pilot.press("escape")
        assert omni.value == ""


async def test_omnibox_execute_help_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_help_command(self) -> None:
            messages.append("help")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "help"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_about_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_about_command(self) -> None:
            messages.append("about")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "about"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_quit_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_quit_command(self) -> None:
            messages.append("quit")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "quit"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_bookmarks_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_bookmarks_command(self) -> None:
            messages.append("bookmarks")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "bookmarks"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_history_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_history_command(self) -> None:
            messages.append("history")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "history"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_contents_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_contents_command(self) -> None:
            messages.append("contents")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "contents"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_execute_local_via_submit() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_local_files_command(self) -> None:
            messages.append("local")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "local"
        await pilot.press("enter")
        assert len(messages) == 1


async def test_omnibox_non_command_does_not_post() -> None:
    from textual.app import App, ComposeResult

    messages = []

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox()

        def on_omnibox_help_command(self) -> None:
            messages.append("help")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.value = "notacommand"
        await pilot.press("enter")
        assert len(messages) == 0


async def test_omnibox_search_returns_results(temp_md_files) -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox(id="omni")

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        omni = pilot.app.query_one(Omnibox)
        results = omni._search_files("python", limit=5)
        assert any("python" in str(r) for _, r in results)
        results = omni._search_files("git", limit=5)
        assert any("git" in str(r) for _, r in results)


async def test_omnibox_down_arrow_stays_focused_without_handler() -> None:
    from textual.app import App, ComposeResult

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Omnibox(id="omni")

    async with TestApp().run_test() as pilot:
        omni = pilot.app.query_one(Omnibox)
        omni.focus()
        await pilot.press("down")
        assert omni.has_focus
