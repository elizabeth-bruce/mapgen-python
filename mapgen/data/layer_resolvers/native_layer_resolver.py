import importlib.util
import os

# import sys

from mapgen.models import Layer
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_resolvers.layer_resolver import LayerResolver


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

        layer = Layer(layer_configuration.name, resolver_fn)

        return layer
