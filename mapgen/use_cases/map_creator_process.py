from collections.abc import Iterable

from typing import Any, Dict

from mapgen.models import LayerFn, MapAccessor, MapCoordinate


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

    def process_map_coordinate(self, map_coordinate: MapCoordinate) -> Any:
        if map_coordinate_val := self.map_accessor[map_coordinate]:
            return map_coordinate_val

        (x, y, layer_name) = map_coordinate

        layer_fn = self.layer_fn_map[layer_name]
        map_coordinate_val = layer_fn(x, y, self.process_map_coordinate)

        self.map_accessor[map_coordinate] = map_coordinate_val

        return map_coordinate_val

    def process_map_coordinates(
        self, map_coordinates: Iterable[MapCoordinate]
    ) -> None:
        for map_coordinate in map_coordinates:
            self.process_map_coordinate(map_coordinate)
