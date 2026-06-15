from __future__ import annotations

from dataclasses import asdict, dataclass, field
from functools import lru_cache
from json import dumps, loads
from pathlib import Path

from xdg import xdg_config_home


@dataclass
class Config:
    light_mode: bool = False
    """Should we run in light mode?"""

    markdown_extensions: list[str] = field(default_factory=lambda: [".md", ".markdown"])
    """What Markdown extensions will we look for?"""

    navigation_left: bool = True
    """Should navigation be docked to the left side of the screen?"""


def config_file() -> Path:
    (config_dir := xdg_config_home() / "scientia-omnibus").mkdir(
        parents=True, exist_ok=True
    )
    return config_dir / "configuration.json"


def save_config(config: Config) -> Config:
    load_config.cache_clear()
    config_file().write_text(dumps(asdict(config), indent=4))
    return load_config()


@lru_cache(maxsize=None)
def load_config() -> Config:
    source_file = config_file()
    return (
        Config(**loads(source_file.read_text()))
        if source_file.exists()
        else save_config(Config())
    )
