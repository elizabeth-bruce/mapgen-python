from abc import ABC, abstractmethod

from mapgen.models import DefinedLayer
from mapgen.data.models import LayerConfiguration, MapContext


class LayerGenerator(ABC):
    @abstractmethod
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> DefinedLayer:
        pass
