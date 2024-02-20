from abc import ABC, abstractmethod

from mapgen.models import Layer
from mapgen.data.models import LayerConfiguration, MapContext


class LayerResolver(ABC):
    @abstractmethod
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> Layer:
        pass
