from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from mapgen.models import Map

T = TypeVar("T")


class MapViewer(ABC, Generic[T]):
    @abstractmethod
    def render(self, target_map: Map, view: str = "default") -> T:
        pass
