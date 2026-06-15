"""Provides useful dialogs for the application."""

from src.dialogs.error import ErrorDialog
from src.dialogs.help_dialog import HelpDialog
from src.dialogs.information import InformationDialog
from src.dialogs.input_dialog import InputDialog
from src.dialogs.yes_no_dialog import YesNoDialog

__all__ = [
    "ErrorDialog",
    "InformationDialog",
    "InputDialog",
    "HelpDialog",
    "YesNoDialog",
]
