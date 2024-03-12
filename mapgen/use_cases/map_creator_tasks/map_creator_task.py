from abc import ABC, abstractmethod

from mapgen.models import MapDefinition


class MapCreatorTask(ABC):
    @abstractmethod
    def populate(self, map_accessor: MapDefinition):
        pass
