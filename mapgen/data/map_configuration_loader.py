from abc import ABC, abstractmethod

from mapgen.data.models import MapConfiguration, MapContext


class MapConfigurationLoader(ABC):
    @abstractmethod
    def load_map_configuration(self) -> MapConfiguration:
        pass

    @abstractmethod
    def load_map_context(self) -> MapContext:
        pass
