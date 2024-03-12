from mapgen.models import UserDefinedFnLayer, TileAttributeAccessor

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


class TestLayerResolver(LayerResolver):
    @staticmethod
    def resolver_fn(x: int, y: int, accessor: TileAttributeAccessor) -> int:
        return x + y

    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> UserDefinedFnLayer:
        layer = UserDefinedFnLayer(
            name=layer_configuration.name,
            type="int",
            fn=TestLayerResolver.resolver_fn,
        )

        return layer
