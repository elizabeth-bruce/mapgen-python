from typing import Dict, Any, List
from typing_extensions import Self

from dataclasses import field

from pydantic import BaseModel, model_validator, ValidationError
from pydantic.dataclasses import dataclass

from mapgen.data.errors import UnknownLayerGeneratorException, InvalidContextException


class FrequencyFilteredNoiseContext(BaseModel):
    roughness: float
    decay_x: float
    decay_y: float
    decay_x_y: float


class LuaContext(BaseModel):
    type: str
    filename: str


class EmptyContext(BaseModel):
    pass


@dataclass
class LayerConfiguration:
    name: str
    generator: str
    context: Dict[str, Any] = field(default_factory=dict)

    @model_validator(mode="after")
    def context_must_adhere_to_generator(self) -> Self:
        context_dict = {
            "LUA": LuaContext,
            "FREQUENCY_FILTERED_NOISE": FrequencyFilteredNoiseContext,
            "test_generator": EmptyContext,
            "native_generator": EmptyContext,
        }

        if self.generator not in context_dict:
            raise UnknownLayerGeneratorException()

        context_cls = context_dict[self.generator]

        try:
            context_cls.model_validate(self.context)  # type: ignore
            return self
        except ValidationError as exc:
            raise InvalidContextException(exc)


@dataclass
class MapConfiguration:
    name: str
    width: int
    height: int
    layer_configurations: List[LayerConfiguration]
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ViewConfiguration:
    name: str
    type: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ViewConfigurationSet:
    view_configurations: List[ViewConfiguration]


@dataclass
class MapContext:
    file_path: str


@dataclass
class ViewSetContext:
    file_path: str
