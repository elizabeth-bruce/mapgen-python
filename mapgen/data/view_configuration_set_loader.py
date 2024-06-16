from abc import ABC, abstractmethod

from mapgen.data.models import ViewConfigurationSet, ViewSetContext


class ViewConfigurationSetLoader(ABC):
    @abstractmethod
    def load(self) -> ViewConfigurationSet:
        pass

    @abstractmethod
    def load_view_set_context(self) -> ViewSetContext:
        pass
