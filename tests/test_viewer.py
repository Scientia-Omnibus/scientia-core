from __future__ import annotations

from pathlib import Path

from widgets.viewer import History


async def test_history_remember_and_location() -> None:
    h = History()
    assert h.location is None
    h.remember(Path("/a/b.md"))
    assert h.location == Path("/a/b.md")
    h.remember(Path("/c/d.md"))
    assert h.location == Path("/c/d.md")


async def test_history_back() -> None:
    h = History()
    h.remember(Path("/a.md"))
    h.remember(Path("/b.md"))
    assert h.back()
    assert h.location == Path("/a.md")
    assert not h.back()
    assert h.location == Path("/a.md")


async def test_history_forward() -> None:
    h = History()
    h.remember(Path("/a.md"))
    h.remember(Path("/b.md"))
    h.back()
    assert h.location == Path("/a.md")
    assert h.forward()
    assert h.location == Path("/b.md")
    assert not h.forward()
    assert h.location == Path("/b.md")


async def test_history_current() -> None:
    h = History()
    assert h.current is None
    h.remember(Path("/a.md"))
    assert h.current == 0
    h.remember(Path("/b.md"))
    assert h.current == 1


async def test_history_locations() -> None:
    h = History()
    h.remember(Path("/a.md"))
    h.remember(Path("/b.md"))
    assert h.locations == [Path("/a.md"), Path("/b.md")]


async def test_history_delete() -> None:
    h = History()
    h.remember(Path("/a.md"))
    h.remember(Path("/b.md"))
    h.remember(Path("/c.md"))
    del h[1]
    assert h.locations == [Path("/a.md"), Path("/c.md")]


async def test_history_clear() -> None:
    h = History()
    h.remember(Path("/a.md"))
    assert h.location is not None
    h2 = History([])
    assert h2.location is None


async def test_viewer_has_markdown_widget() -> None:
    from textual.app import App, ComposeResult
    from widgets.viewer import Viewer

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Viewer()

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        viewer = pilot.app.query_one(Viewer)
        assert viewer.document is not None


async def test_viewer_back_forward() -> None:
    from textual.app import App, ComposeResult
    from widgets.viewer import Viewer

    class TestApp(App):
        def compose(self) -> ComposeResult:
            yield Viewer()

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        viewer = pilot.app.query_one(Viewer)
        assert viewer.location is None
        viewer.back()
        viewer.forward()
