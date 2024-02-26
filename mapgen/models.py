from typing import Any, Callable, Dict, List, Tuple

from dataclasses import dataclass

type TileCoordinate = Tuple[int, int]  # type: ignore
type MapCoordinate = Tuple[int, int, str]  # type: ignore

type TileAttributeAccessor = Callable[  # type: ignore
    MapCoordinate, Any
]  # type: ignore
type LayerFn = Callable[  # type: ignore
    [int, int, TileAttributeAccessor], Any
]  # type: ignore


@dataclass
class Layer:
    name: str
    fn: LayerFn


type MapCoordinateSet = Dict[MapCoordinate, Any]  # type: ignore


@dataclass
class MapDefinition:
    name: str
    width: int
    height: int
    layers: List[Layer]


@dataclass
class Map:
    map_definition: MapDefinition
    map_coordinates: MapCoordinateSet
