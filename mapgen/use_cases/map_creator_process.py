from collections.abc import Iterable

from typing import Any, Dict, Set

from functools import partial

from mapgen.models import LayerFn, MapAccessor, MapCoordinate
from mapgen.use_cases.exceptions import CircularDependencyException


class MapCreatorProcess:
    def __init__(
        self,
        map_accessor: MapAccessor,
        layer_fn_map: Dict[str, LayerFn],
        logger,
    ):
        self.map_accessor = map_accessor
        self.layer_fn_map = layer_fn_map
        self.logger = logger

    def process_map_coordinate(
        self,
        dependent_coordinates: Set[MapCoordinate],
        map_coordinate: MapCoordinate,
    ) -> Any:
        if map_coordinate in dependent_coordinates:
            raise CircularDependencyException(
                f"Map coordinate {map_coordinate} has circular dependency!"
            )
        if map_coordinate_val := self.map_accessor[map_coordinate]:
            return map_coordinate_val

        (x, y, layer_name) = map_coordinate

        layer_fn = self.layer_fn_map[layer_name]

        dependent_coordinates.add(map_coordinate)
        next_accessor = partial(self.process_map_coordinate, dependent_coordinates)
        map_coordinate_val = layer_fn(x, y, next_accessor)

        self.map_accessor[map_coordinate] = map_coordinate_val

        return map_coordinate_val

    def process_map_coordinates(
        self, map_coordinates: Iterable[MapCoordinate]
    ) -> None:
        for map_coordinate in map_coordinates:
            self.process_map_coordinate(set(), map_coordinate)
