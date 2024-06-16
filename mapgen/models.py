from numpy.typing import NDArray

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
class LayerMetadata:
    name: str
    type: str


@dataclass
class MapMetadata:
    name: str
    width: int
    height: int
    layers: List[LayerMetadata]


@dataclass(kw_only=True)
class Layer:
    name: str
    type: str

    def to_layer_metadata(self) -> LayerMetadata:
        return LayerMetadata(name=self.name, type=self.type)


@dataclass(kw_only=True)
class UserDefinedFnLayer(Layer):
    layer_type: str = "USER_DEFINED_FN"
    fn: LayerFn


@dataclass(kw_only=True)
class FrequencyFilteredNoiseLayer(Layer):
    layer_type: str = "FREQUENCY_FILTERED_NOISE"
    decay_x: float
    decay_y: float
    decay_x_y: float
    roughness: float


type DefinedLayer = FrequencyFilteredNoiseLayer | UserDefinedFnLayer  # type: ignore
type MapCoordinateSet = Dict[MapCoordinate, Any]  # type: ignore


class MapAccessor(ABC):
    @abstractmethod
    def __getitem__(self, key: MapCoordinate) -> Any:
        pass

    @abstractmethod
    def __setitem__(self, key: MapCoordinate, val: Any) -> None:
        pass

    @abstractmethod
    def get_raw_values(self, layer_name: str) -> NDArray[Any]:
        pass


@dataclass
class MapDefinition:
    name: str
    width: int
    height: int
    layers: List[DefinedLayer]

    def to_map_metadata(self) -> MapMetadata:
        return MapMetadata(
            name=self.name,
            width=self.width,
            height=self.height,
            layers=[layer.to_layer_metadata() for layer in self.layers],
        )


@dataclass
class Map:
    map_metadata: MapMetadata
    map_accessor: MapAccessor
