from typing import Any, Callable, Dict, List, Tuple

from abc import ABC, abstractmethod

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
    type: str
    fn: LayerFn


type MapCoordinateSet = Dict[MapCoordinate, Any]  # type: ignore


class MapAccessor(ABC):
    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def __setitem__(self, key, val):
        pass


@dataclass
class MapDefinition:
    name: str
    width: int
    height: int
    layers: List[Layer]


@dataclass
class Map:
    map_definition: MapDefinition
    map_accessor: MapAccessor
