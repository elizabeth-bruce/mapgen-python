from abc import ABC, abstractmethod

from numpy.random import RandomState

from mapgen.models import MapDefinition


class MapCreatorTask(ABC):
    @abstractmethod
    def populate(self, map_accessor: MapDefinition, random_state: RandomState) -> None:
        pass
