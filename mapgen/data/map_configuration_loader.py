from typing import Any, Dict

from abc import ABC, abstractmethod

from mapgen.data.models import MapConfiguration, MapContext


class MapConfigurationLoader(ABC):
    @abstractmethod
    def load_map_configuration() -> MapConfiguration:
        pass

    @abstractmethod
    def load_map_context() -> MapContext:
        pass
