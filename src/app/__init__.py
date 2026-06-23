__author__ = "Scientia Omnibus"
__email__ = "levmarkpost@gmail.com"
__version__ = "0.1.9"
__licence__ = "MIT"


def run() -> None:
    from app.app import run as _run

    _run()


__all__ = ["run"]
