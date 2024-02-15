from typing import Dict, Type

from mapgen.models import Layer
from mapgen.data.models import LayerConfiguration
from mapgen.data.errors import UnknownLayerResolverException
from mapgen.data.layer_resolvers import LayerResolver, TestLayerResolver


class LayerConfigurationLoader:
    layer_resolver_type_map: Dict[str, Type[LayerResolver]] = {
        "test_resolver": TestLayerResolver
    }

    def load(self, layer_configuration: LayerConfiguration) -> Layer:
        resolver_type = layer_configuration.layer_type
        resolver_class = LayerConfigurationLoader.layer_resolver_type_map.get(
            resolver_type, None
        )

        if not resolver_class:
            raise UnknownLayerResolverException(
                f"Resolver type {resolver_type} not found"
            )

        resolver = resolver_class()

        layer = resolver.resolve(layer_configuration)

        return layer
