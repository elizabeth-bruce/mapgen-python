from typing import Dict, Any, List

from dataclasses import dataclass, field


@dataclass
class LayerConfiguration:
    name: str
    generator: str
    context: Dict[str, Any] = field(default_factory=dict)


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
