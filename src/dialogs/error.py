from textual.widgets._button import ButtonVariant

from dialogs.text_dialog import TextDialog


class ErrorDialog(TextDialog):
    DEFAULT_CSS = """
    ErrorDialog > Vertical {
        background: $error 15%;
        border: thick $error 50%;
    }

    ErrorDialog #message {
        border-top: solid $error 25%;
        border-bottom: solid $error 25%;
    }
    """

    @property
    def button_style(self) -> ButtonVariant:
        return "error"
