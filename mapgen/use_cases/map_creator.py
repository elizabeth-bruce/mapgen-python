import multiprocessing as mp

from typing import Any, Callable, List
from collections.abc import Iterable

from mapgen.models import MapDefinition, Map, MapCoordinate

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.map_creator_process import MapCreatorProcess

NUM_THREADS = 8

logger = mp.log_to_stderr()


def cycle_generator(
    gf: Callable[[], Iterable[Any]], n: int
) -> List[Iterable[Any]]:
    def get_kth_term_of_generator(g, n, k):
        return (t for i, t in enumerate(g) if i % n == k)

    return [get_kth_term_of_generator(gf(), n, k) for k in range(0, n)]


class MapCreator:
    def create_map(self, map_definition: MapDefinition) -> Map:
        map_accessor = SharedMemoryMapAccessor(map_definition)
        layer_fn_map = {
            layer.name: layer.fn for layer in map_definition.layers
        }

        layer_names = list(layer_fn_map.keys())

        map_creator_process = MapCreatorProcess(
            map_accessor, layer_fn_map, logger
        )

        def get_map_coordinate_generator() -> Iterable[MapCoordinate]:
            return (
                (x, y, layer_name)
                for x in range(0, map_definition.width)
                for y in range(0, map_definition.height)
                for layer_name in layer_names
            )

        map_coordinate_groups = cycle_generator(
            get_map_coordinate_generator, NUM_THREADS
        )

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
