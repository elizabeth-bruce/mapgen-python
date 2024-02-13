from typing import Any, Awaitable, Callable, Dict, List, Tuple

from dataclasses import dataclass


@dataclass
class Layer:
    name: str
    fn: Callable[[int, int], Awaitable[Any]]


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


@dataclass(kw_only=True)
class LayerResolverConfiguration:
    name: str


@dataclass(kw_only=True)
class NativeLayerResolverConfiguration(LayerResolverConfiguration):
    resolver_fn: Callable[[int, int], Awaitable[Any]]


@dataclass
class LayerConfiguration:
    name: str
    resolver: LayerResolverConfiguration


@dataclass
class MapConfiguration:
    width: int
    height: int
    name: str
    layer_configurations: List[LayerConfiguration]
