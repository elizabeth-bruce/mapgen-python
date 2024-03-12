from mapgen.models import MapDefinition, Map

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_tasks.user_defined_fn_map_creator_task import (
    UserDefinedFnMapCreatorTask,
)


class MapCreator:
    def create_map(self, map_definition: MapDefinition) -> Map:
        map_accessor = SharedMemoryMapAccessor(map_definition)

        user_defined_fn_map_creator_task = UserDefinedFnMapCreatorTask(map_accessor)
        user_defined_fn_map_creator_task.populate(map_definition)

        return Map(map_definition=map_definition, map_accessor=map_accessor)
