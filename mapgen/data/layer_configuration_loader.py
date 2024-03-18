from typing import Dict, Type

from mapgen.models import DefinedLayer
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.errors import UnknownLayerGeneratorException
from mapgen.data.layer_generators import (
    LayerGenerator,
    NativeLayerGenerator,
    TestLayerGenerator,
    FrequencyFilteredNoiseLayerGenerator,
)


class LayerConfigurationLoader:
    layer_generator_type_map: Dict[str, Type[LayerGenerator]] = {
        "test_generator": TestLayerGenerator,
        "native_generator": NativeLayerGenerator,
        "FREQUENCY_FILTERED_NOISE": FrequencyFilteredNoiseLayerGenerator,
    }

    def load(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> DefinedLayer:
        generator_type = layer_configuration.generator
        generator_class = LayerConfigurationLoader.layer_generator_type_map.get(
            generator_type, None
        )

        if not generator_class:
            raise UnknownLayerGeneratorException(f"Generator type {generator_type} not found")

        generator = generator_class()

        layer = generator.resolve(layer_configuration, map_context)

        return layer
