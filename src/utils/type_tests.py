from functools import singledispatch
from pathlib import Path
from typing import Any

from data.config import load_config


@singledispatch
def maybe_markdown(resource: Any) -> bool:
    del resource
    return False


@maybe_markdown.register
def _(resource: Path) -> bool:
    return resource.suffix.lower() in load_config().markdown_extensions


@maybe_markdown.register
def _(resource: str) -> bool:
    return maybe_markdown(Path(resource))
