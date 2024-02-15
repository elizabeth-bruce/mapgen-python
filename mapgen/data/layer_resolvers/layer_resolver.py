from abc import ABC, abstractmethod

from mapgen.models import Layer


class LayerResolver(ABC):
    @abstractmethod
    def resolve(self, layer_configuration) -> Layer:
        pass
