from mapgen.models import Layer, TileAttributeAccessor

from mapgen.data.models import LayerConfiguration
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


class NativeLayerResolver(LayerResolver):
    @staticmethod
    async def resolver_fn(
        x: int, y: int, accessor: TileAttributeAccessor
    ) -> int:
        return x + y

    def resolve(self, layer_configuration: LayerConfiguration) -> Layer:
        layer = Layer(
            layer_configuration.name, NativeLayerResolver.resolver_fn
        )

        return layer
