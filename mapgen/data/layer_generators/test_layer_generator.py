from mapgen.models import UserDefinedFnLayer, TileAttributeAccessor

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.layer_generator import LayerGenerator


class TestLayerGenerator(LayerGenerator):
    @staticmethod
    def generator_fn(x: int, y: int, accessor: TileAttributeAccessor) -> int:
        return x + y

    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> UserDefinedFnLayer:
        layer = UserDefinedFnLayer(
            name=layer_configuration.name,
            type="int",
            fn=TestLayerGenerator.generator_fn,
        )

        return layer
