from mapgen.models import FrequencyFilteredNoiseLayer

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.layer_generator import LayerGenerator

TYPE = "float"


class FrequencyFilteredNoiseLayerGenerator(LayerGenerator):
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> FrequencyFilteredNoiseLayer:
        layer = FrequencyFilteredNoiseLayer(
            name=layer_configuration.name,
            type=TYPE,
            decay_x=layer_configuration.context["decay_x"],
            decay_y=layer_configuration.context["decay_y"],
            decay_x_y=layer_configuration.context["decay_x_y"],
            roughness=layer_configuration.context["roughness"],
        )

        return layer
