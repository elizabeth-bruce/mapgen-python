import importlib.util
import os

from typing import Any

from mapgen.models import UserDefinedFnLayer, TileAttributeAccessor
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.layer_generator import LayerGenerator


class LazyAccessorTile:
    def __init__(self, x: int, y: int, tile_attribute_accessor: TileAttributeAccessor):
        self.x = x
        self.y = y
        self.tile_attribute_accessor = tile_attribute_accessor

    def __getattr__(self, attr: str):
        map_coordinate = (self.x, self.y, attr)
        return self.tile_attribute_accessor(map_coordinate)


class NativeLayerGenerator(LayerGenerator):
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> UserDefinedFnLayer:
        layer_context = layer_configuration.context
        file_path = os.path.join(map_context.file_path, layer_context["filename"])

        module_name = "mapgen_layer_generator"

        spec = importlib.util.spec_from_file_location(module_name, file_path)

        assert spec is not None, f"No Python code found at location {file_path}"
        module = importlib.util.module_from_spec(spec)

        assert (
            spec.loader is not None
        ), f"Python code found at location {file_path} could not be imported"

        module = importlib.util.module_from_spec(spec)

        assert (
            module is not None
        ), f"Python code at location {file_path} could not be imported"

        spec.loader.exec_module(module)

        generator_fn = getattr(module, layer_configuration.name)

        def layer_fn(x: int, y: int, accessor: TileAttributeAccessor) -> Any:
            def get_tile(x, y):
                return LazyAccessorTile(x, y, accessor)

            return generator_fn(x, y, get_tile)

        layer = UserDefinedFnLayer(
            name=layer_configuration.name,
            type=layer_configuration.context["type"],
            fn=layer_fn,
        )

        return layer
