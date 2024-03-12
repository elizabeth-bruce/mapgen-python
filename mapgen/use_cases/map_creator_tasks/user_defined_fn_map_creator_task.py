import multiprocessing as mp
from collections.abc import Iterable

from typing import List

from mapgen.models import MapAccessor, MapCoordinate, MapDefinition, UserDefinedFnLayer
from mapgen.use_cases.map_creator_tasks.map_creator_task import MapCreatorTask

from mapgen.use_cases.map_creator_process import MapCreatorProcess

NUM_PROCESSES = 4

logger = mp.log_to_stderr()


class UserDefinedFnMapCreatorTask(MapCreatorTask):
    def __init__(self, map_accessor: MapAccessor):
        self.map_accessor = map_accessor

    @staticmethod
    def get_layers_to_populate(
        map_definition: MapDefinition,
    ) -> List[UserDefinedFnLayer]:
        return [
            layer  # type: ignore
            for layer in map_definition.layers
            if layer.layer_type == "USER_DEFINED_FN"
        ]

    @staticmethod
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

    def populate(self, map_definition: MapDefinition) -> None:
        layers = UserDefinedFnMapCreatorTask.get_layers_to_populate(map_definition)

        layer_fn_map = {layer.name: layer.fn for layer in layers}

        map_creator_process = MapCreatorProcess(
            self.map_accessor, layer_fn_map, logger
        )

        map_coordinate_groups = [
            UserDefinedFnMapCreatorTask.get_map_coordinates(
                map_definition, NUM_PROCESSES, i
            )
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
