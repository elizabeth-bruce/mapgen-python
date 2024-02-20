from typing import Any, Awaitable, Callable, Dict, List, Tuple

from dataclasses import dataclass

type TileCoordinate = Tuple[int, int]  # type: ignore
type TileLayerCoordinate = Tuple[int, int, str]  # type: ignore

type TileAttributeAccessor = Callable[  # type: ignore
    TileLayerCoordinate, Awaitable[Any]
]  # type: ignore
type LayerFn = Callable[  # type: ignore
    [int, int, TileAttributeAccessor], Awaitable[Any]
]  # type: ignore


@dataclass
class Layer:
    name: str
    fn: LayerFn


type TileSet = Dict[TileLayerCoordinate, Any]  # type: ignore


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
