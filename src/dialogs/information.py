from src.dialogs.text_dialog import TextDialog


class InformationDialog(TextDialog):
    DEFAULT_CSS = """
    InformationDialog > Vertical {
        border: thick $primary 50%;
    }
    """
