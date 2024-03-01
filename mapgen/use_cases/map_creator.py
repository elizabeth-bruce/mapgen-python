import multiprocessing as mp

from collections.abc import Iterable

from mapgen.models import MapDefinition, Map, MapCoordinate

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_process import MapCreatorProcess

NUM_PROCESSES = 8

logger = mp.log_to_stderr()


def get_map_coordinates(
    map_definition: MapDefinition, period: int, offset: int
) -> Iterable[MapCoordinate]:
    layer_names = [layer.name for layer in map_definition.layers]
    num_layers = len(layer_names)
    width = map_definition.width
    height = map_definition.height

    return (
        (
            (idx // num_layers) % width,
            idx // (width * num_layers),
            layer_names[idx % num_layers],
        )
        for idx in range(offset, num_layers * width * height, period)
    )


class MapCreator:
    def create_map(self, map_definition: MapDefinition) -> Map:
        map_accessor = SharedMemoryMapAccessor(map_definition)
        layer_fn_map = {
            layer.name: layer.fn for layer in map_definition.layers
        }

        map_creator_process = MapCreatorProcess(
            map_accessor, layer_fn_map, logger
        )

        map_coordinate_groups = [
            get_map_coordinates(map_definition, NUM_PROCESSES, i)
            for i in range(0, NUM_PROCESSES)
        ]

        def create_process(map_coordinates: Iterable[MapCoordinate]):
            return mp.Process(
                target=map_creator_process.process_map_coordinates,
                args=(map_coordinates,),
            )

        processes = [
            create_process(map_coordinates)
            for map_coordinates in map_coordinate_groups
        ]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        return Map(map_definition=map_definition, map_accessor=map_accessor)
