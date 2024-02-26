import importlib.util
import os

from typing import Any

from async_lru import alru_cache

from mapgen.models import Layer, TileAttributeAccessor
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


class LazyAccessorTile:
    def __init__(
        self, x: int, y: int, tile_attribute_accessor: TileAttributeAccessor
    ):
        self.x = x
        self.y = y
        self.tile_attribute_accessor = tile_attribute_accessor

    def __getattr__(self, attr: str):
        return self.tile_attribute_accessor((self.x, self.y, attr))


class NativeLayerResolver(LayerResolver):
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> Layer:
        layer_context = layer_configuration.context
        file_path = os.path.join(
            map_context.file_path, layer_context["filename"]
        )

        module_name = "mapgen_layer_resolver"

        spec = importlib.util.spec_from_file_location(module_name, file_path)

        assert (
            spec is not None
        ), f"No Python code found at location {file_path}"
        module = importlib.util.module_from_spec(spec)

        assert (
            spec.loader is not None
        ), f"Python code found at location {file_path} could not be imported"

        module = importlib.util.module_from_spec(spec)

        assert (
            module is not None
        ), f"Python code at location {file_path} could not be imported"

        spec.loader.exec_module(module)

        resolver_fn = getattr(module, layer_configuration.name)

        async def layer_fn(
            x: int, y: int, accessor: TileAttributeAccessor
        ) -> Any:
            def get_tile(x, y):
                return LazyAccessorTile(x, y, accessor)

            return await resolver_fn(x, y, get_tile)

        cached_fn = alru_cache(layer_fn)

        layer = Layer(layer_configuration.name, cached_fn)

        return layer
