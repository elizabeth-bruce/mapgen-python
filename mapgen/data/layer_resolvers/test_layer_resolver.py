from mapgen.models import Layer, TileAttributeAccessor

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


class TestLayerResolver(LayerResolver):
    @staticmethod
    def resolver_fn(x: int, y: int, accessor: TileAttributeAccessor) -> int:
        return x + y

    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> Layer:
        layer = Layer(
            layer_configuration.name, "int", TestLayerResolver.resolver_fn
        )

        return layer
