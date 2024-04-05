from abc import ABC, abstractmethod

from mapgen.models import Map


class MapLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> Map:
        pass
