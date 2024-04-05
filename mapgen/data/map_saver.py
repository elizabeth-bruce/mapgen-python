from abc import ABC, abstractmethod

from mapgen.models import Map


class MapSaver(ABC):
    @abstractmethod
    def save(self, save_map: Map, path: str) -> None:
        pass
