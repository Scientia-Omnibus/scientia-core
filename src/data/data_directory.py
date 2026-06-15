from pathlib import Path

from xdg import xdg_data_home


def data_directory() -> Path:
    (target_directory := xdg_data_home() / "scientia-omnibus").mkdir(
        parents=True, exist_ok=True
    )
    return target_directory
