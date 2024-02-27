from typing import Dict, Any, List

from dataclasses import dataclass, field


@dataclass
class LayerConfiguration:
    name: str
    type: str
    resolver: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MapConfiguration:
    name: str
    width: int
    height: int
    layer_configurations: List[LayerConfiguration]
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MapContext:
    file_path: str
