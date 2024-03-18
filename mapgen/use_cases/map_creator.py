from numpy.random import RandomState

from mapgen.models import MapDefinition, Map

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_tasks.user_defined_fn_map_creator_task import (
    UserDefinedFnMapCreatorTask,
)

from mapgen.use_cases.map_creator_tasks.frequency_filtered_noise_map_creator_task import (
    FrequencyFilteredNoiseMapCreatorTask,
)


class MapCreator:
    def create_map(self, map_definition: MapDefinition, seed: int) -> Map:
        map_accessor = SharedMemoryMapAccessor(map_definition)

        random_state = RandomState(seed)

        frequency_filtered_noise_map_creator_task = FrequencyFilteredNoiseMapCreatorTask(
            map_accessor
        )
        frequency_filtered_noise_map_creator_task.populate(map_definition, random_state)

        user_defined_fn_map_creator_task = UserDefinedFnMapCreatorTask(map_accessor)
        user_defined_fn_map_creator_task.populate(map_definition, random_state)

        return Map(map_definition=map_definition, map_accessor=map_accessor)
