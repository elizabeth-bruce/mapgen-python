from typing import Any, Dict

from mapgen.models import MapDefinition, Map, MapCoordinate, MapCoordinateSet

NUM_THREADS = 8


class MapCreator:
    def __init__(self):
        self.map_coordinates: Dict[MapCoordinate, Any] = {}

    def get_uncreated_map_coordinates(self):
        for map_coordinate in self.all_map_coordinates:
            if map_coordinate not in self.map_coordinates:
                yield map_coordinate

    def get_map_coordinate_value(self, map_coordinate: MapCoordinate) -> Any:
        if map_coordinate in self.map_coordinates:
            return self.map_coordinates[map_coordinate]

        (x, y, layer_name) = map_coordinate
        layers = self.map_definition.layers

        layer = next((layer for layer in layers if layer.name == layer_name))

        fn = layer.fn

        map_coordinate_value = fn(x, y, self.get_map_coordinate_value)

        self.map_coordinates[map_coordinate] = map_coordinate_value

        return map_coordinate_value

    def create_map_coordinate_set(
        self, map_definition: MapDefinition
    ) -> MapCoordinateSet:
        self.all_map_coordinates = (
            (x, y, layer_name)
            for x in range(0, map_definition.width)
            for y in range(0, map_definition.height)
            for layer_name in [layer.name for layer in map_definition.layers]
        )

        for map_coordinate in self.all_map_coordinates:
            self.get_map_coordinate_value(map_coordinate)

        return self.map_coordinates

    def create_map(self, map_definition: MapDefinition) -> Map:
        self.map_definition = map_definition

        self.create_map_coordinate_set(self.map_definition)

        return Map(
            map_definition=map_definition,
            map_coordinates=self.map_coordinates,
        )
