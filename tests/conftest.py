from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from pytest import MonkeyPatch

from data.config import Config


@pytest.fixture(autouse=True)
def _patch_dependencies(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> Generator[None, None, None]:
    import data
    import data.config as data_config
    import data.data_directory as data_dir_mod
    import utils.update_utils as update_utils
    import widgets.omnibox as omnibox_mod
    import widgets.navigation as nav_mod
    import screens.main as main_mod
    import data.bookmarks as bookmarks_data_mod
    import data.history as history_data_mod

    mock_config = Config()

    def mock_load() -> Config:
        return mock_config

    monkeypatch.setattr(omnibox_mod, "data_directory", lambda: tmp_path)
    monkeypatch.setattr(data_dir_mod, "data_directory", lambda: tmp_path)
    monkeypatch.setattr(bookmarks_data_mod, "data_directory", lambda: tmp_path)
    monkeypatch.setattr(history_data_mod, "data_directory", lambda: tmp_path)
    monkeypatch.setattr(data_config, "load_config", mock_load)
    monkeypatch.setattr(data, "load_config", mock_load)
    monkeypatch.setattr(main_mod, "load_config", mock_load)
    monkeypatch.setattr(nav_mod, "load_config", mock_load)
    monkeypatch.setattr(update_utils, "check_internet_connection", lambda: False)
    monkeypatch.setattr(update_utils, "get_local_version", lambda: "0.1.8")
    monkeypatch.setattr(
        main_mod, "check_internet_connection", lambda: False, raising=False
    )
    monkeypatch.setattr(main_mod, "compare_versions", lambda _a, _b: 0, raising=False)  # noqa: E731

    def mock_save(_c: object) -> Config:
        return mock_config

    monkeypatch.setattr(data, "save_config", mock_save)

    monkeypatch.setattr(main_mod, "save_config", mock_save)
    monkeypatch.setattr(nav_mod, "save_config", mock_save)

    monkeypatch.setattr(main_mod, "load_history", lambda: [])
    monkeypatch.setattr(data, "load_history", lambda: [])

    yield


@pytest.fixture
def temp_md_files(tmp_path: Path) -> list[Path]:
    dirs = {
        "languages/python",
        "languages/rust",
        "tools/git",
        "concepts/testing",
    }
    files = []
    for subdir in dirs:
        d = tmp_path / subdir
        d.mkdir(parents=True, exist_ok=True)
        name = subdir.split("/")[-1]
        p = d / f"{name}.md"
        p.write_text(f"# {name}")
        files.append(p)
    extra = tmp_path / "README.md"
    extra.write_text("# Root readme")
    files.append(extra)
    non_md = tmp_path / "notes.txt"
    non_md.write_text("not markdown")
    return files
