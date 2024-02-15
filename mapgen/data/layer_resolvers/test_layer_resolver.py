from mapgen.models import Layer

from mapgen.data.models import LayerConfiguration
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


class TestLayerResolver(LayerResolver):
    @staticmethod
    async def resolver_fn(x: int, y: int) -> int:
        return x + y

    def resolve(self, layer_configuration: LayerConfiguration) -> Layer:
        layer = Layer(layer_configuration.name, TestLayerResolver.resolver_fn)

        return layer
