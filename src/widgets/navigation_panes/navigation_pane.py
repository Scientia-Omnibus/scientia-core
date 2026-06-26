from abc import abstractmethod, ABC, ABCMeta

from textual.widgets import TabbedContent, TabPane
from typing_extensions import Self


class NavMeta(ABCMeta, type(TabPane)):
    pass


class NavigationPane(ABC, TabPane, metaclass=NavMeta):
    @abstractmethod
    def set_focus_within(self) -> None:
        pass

    def activate(self) -> Self:
        assert self.parent is not None
        if self.id is not None and isinstance(self.parent.parent, TabbedContent):
            self.parent.parent.active = self.id
        return self
