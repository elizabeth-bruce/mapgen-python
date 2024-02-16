from typing import Any, Awaitable, Callable, Dict, List, Tuple

from dataclasses import dataclass


type TileAttributeAccessor = Callable[  # type: ignore
    [int, int, str], Awaitable[Any]
]  # type: ignore
type LayerFn = Callable[  # type: ignore
    [int, int, TileAttributeAccessor], Awaitable[Any]
]  # type: ignore


@dataclass
class Layer:
    name: str
    fn: LayerFn


@dataclass
class Tile:
    x: int
    y: int
    layer: Layer
    val: Any


type TileSet = Dict[Tuple[int, int, str], Any]  # type: ignore


@dataclass
class MapDefinition:
    name: str
    width: int
    height: int
    layers: List[Layer]


@dataclass
class Map:
    map_definition: MapDefinition
    tiles: TileSet
