from typing import Any, Dict, Union

from multiprocessing import Lock
from multiprocessing.sharedctypes import Array, SynchronizedArray
from ctypes import c_int, c_float, c_char_p

from mapgen.models import MapAccessor, MapCoordinate, MapDefinition
from mapgen.use_cases.exceptions import InvalidMapCoordinateException

ALLOWED_CTYPE = Union[c_int, c_float, c_char_p]

LAYER_TYPE_TO_CTYPE_MAP = {"int": c_int, "float": c_float, "str": c_char_p}


class SharedMemoryMapAccessor(MapAccessor):
    def __init__(self, map_definition: MapDefinition):
        self.width = map_definition.width
        self.height = map_definition.height

        layer_size = self.width * self.height

        self.layer_map_coordinates: Dict[
            str, SynchronizedArray[ALLOWED_CTYPE]
        ] = {}

        for layer in map_definition.layers:
            lock = Lock()
            layer_ctype = LAYER_TYPE_TO_CTYPE_MAP[layer.type]

            self.layer_map_coordinates[layer.name] = Array(
                layer_ctype, layer_size, lock=lock  # type: ignore
            )

    def __getitem__(self, map_coordinate: MapCoordinate) -> Any:
        (x, y, layer_name) = map_coordinate

        layer_map_array = self.layer_map_coordinates.get(layer_name, None)

        if not layer_map_array:
            raise InvalidMapCoordinateException(
                f"Layer name {layer_name} does not exist in map definition"
            )

        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            raise InvalidMapCoordinateException(
                f"Layer coordinate ({x}, {y}) out of bounds of map definition"
            )

        idx = (y * self.width) + x

        return layer_map_array[idx]

    def __setitem__(self, map_coordinate: MapCoordinate, val: Any) -> None:
        (x, y, layer_name) = map_coordinate

        layer_map_array = self.layer_map_coordinates[layer_name]

        if not layer_map_array:
            raise InvalidMapCoordinateException(
                f"Layer name {layer_name} does not exist in map definition"
            )

        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            raise InvalidMapCoordinateException(
                f"Layer coordinate ({x}, {y}) out of bounds of map definition"
            )

        idx = (y * self.width) + x

        layer_map_array[idx] = val
