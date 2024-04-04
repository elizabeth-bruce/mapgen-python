from numpy.random import RandomState

from mapgen.models import Layer, LayerMetadata, Map, MapDefinition, MapMetadata

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_tasks.user_defined_fn_map_creator_task import (
    UserDefinedFnMapCreatorTask,
)

from mapgen.use_cases.map_creator_tasks.frequency_filtered_noise_map_creator_task import (
    FrequencyFilteredNoiseMapCreatorTask,
)


class MapCreator:
    def create_map(self, map_definition: MapDefinition, seed: int) -> Map:
        map_metadata = self.convert_map_definition_to_map_metadata(map_definition)
        map_accessor = SharedMemoryMapAccessor(map_definition)

        random_state = RandomState(seed)

        frequency_filtered_noise_map_creator_task = FrequencyFilteredNoiseMapCreatorTask(
            map_accessor
        )
        frequency_filtered_noise_map_creator_task.populate(map_definition, random_state)

        user_defined_fn_map_creator_task = UserDefinedFnMapCreatorTask(map_accessor)
        user_defined_fn_map_creator_task.populate(map_definition, random_state)

        return Map(map_metadata=map_metadata, map_accessor=map_accessor)

    def convert_map_definition_to_map_metadata(self, map_definition: MapDefinition) -> MapMetadata:
        layers = [
            self.convert_layer_definition_to_layer_metadata(layer)
            for layer
            in map_definition.layers
        ]

        map_metadata = MapMetadata(
            name=map_definition.name,
            width=map_definition.width,
            height=map_definition.height,
            layers=layers
        )

        return map_metadata

    def convert_layer_definition_to_layer_metadata(self, layer: Layer) -> LayerMetadata:
        layer_metadata = LayerMetadata(
            name=layer.name,
            type=layer.type
        )

        return layer_metadata
