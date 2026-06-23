from __future__ import annotations

from typing import Any

from textual.widgets import Button, Input, Label, OptionList, Static

from dialogs import ErrorDialog, HelpDialog, InformationDialog, InputDialog, YesNoDialog
from dialogs.directory_picker import DirectoryPicker
from dialogs.knowledge_sync import KnowledgeSync
from dialogs.progress_screen import ProgressScreen


async def test_error_dialog_shows_title_and_message() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(ErrorDialog("Test Error", "Something went wrong"))

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, ErrorDialog)
        rendered = screen.query_one("#message", Static).render()
        assert "Something went wrong" in str(rendered)


async def test_error_dialog_dismiss_on_button() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(ErrorDialog("Error", "msg"))

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        await pilot.click(Button)
        await pilot.pause()
        assert not isinstance(pilot.app.screen, ErrorDialog)


async def test_error_dialog_dismiss_on_escape() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(ErrorDialog("Error", "msg"))

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, ErrorDialog)


async def test_information_dialog_shows() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(InformationDialog("Info Title", "Info message"))

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, InformationDialog)


async def test_yes_no_dialog_yes_returns_true() -> None:
    from textual.app import App

    result: Any = None

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(YesNoDialog("Question", "Are you sure?"), self._on_result)

        def _on_result(self, value: bool | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.click("#yes")
        await pilot.pause()
    assert result is True


async def test_yes_no_dialog_no_returns_false() -> None:
    from textual.app import App

    result: Any = None

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(
                YesNoDialog("Question", "Are you sure?", yes_first=False),
                self._on_result,
            )

        def _on_result(self, value: bool | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
    assert result is False


async def test_yes_no_dialog_escape_pops_screen() -> None:
    from textual.app import App

    result: Any = "unset"

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(YesNoDialog("Question", "Sure?"), self._on_result)

        def _on_result(self, value: bool | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        assert isinstance(pilot.app.screen, YesNoDialog)
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, YesNoDialog)
        assert result == "unset"


async def test_input_dialog_accept_returns_value() -> None:
    from textual.app import App

    result: Any = None

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(InputDialog("Enter name:", "default"), self._on_result)

        def _on_result(self, value: str | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        inp = pilot.app.screen.query_one(Input)
        inp.value = "new value"
        await pilot.click("#ok")
        await pilot.pause()
    assert result == "new value"


async def test_input_dialog_cancel_pops_screen() -> None:
    from textual.app import App

    result: Any = "unset"

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(InputDialog("Enter name:", "default"), self._on_result)

        def _on_result(self, value: str | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        assert isinstance(pilot.app.screen, InputDialog)
        await pilot.click("#cancel")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, InputDialog)
        assert result == "unset"


async def test_input_dialog_escape_pops_screen() -> None:
    from textual.app import App

    result: Any = "unset"

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(InputDialog("Enter name:", "default"), self._on_result)

        def _on_result(self, value: str | None) -> None:
            nonlocal result
            result = value

    async with TestApp().run_test(size=(80, 24)) as pilot:
        await pilot.pause()
        assert isinstance(pilot.app.screen, InputDialog)
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, InputDialog)
        assert result == "unset"


async def test_help_dialog_renders() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(HelpDialog())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, HelpDialog)


async def test_help_dialog_close_button() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(HelpDialog())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        await pilot.click("Button")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, HelpDialog)


async def test_help_dialog_escape_dismisses() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(HelpDialog())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, HelpDialog)


async def test_help_dialog_f1_dismisses() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(HelpDialog())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        await pilot.press("f1")
        await pilot.pause()
        assert not isinstance(pilot.app.screen, HelpDialog)


async def test_progress_screen_renders() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(ProgressScreen("Loading..."))

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, ProgressScreen)
        assert screen.message == "Loading..."


async def test_directory_picker_renders() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(DirectoryPicker())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, DirectoryPicker)
        assert screen.query_one(Label)
        assert screen.query_one(OptionList)


async def test_knowledge_sync_renders() -> None:
    from textual.app import App

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(KnowledgeSync())

    async with TestApp().run_test() as pilot:
        await pilot.pause()
        screen = pilot.app.screen
        assert isinstance(screen, KnowledgeSync)
        assert len(screen.sciences) > 0
