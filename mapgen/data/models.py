from typing import Dict, Any, List, Optional

from dataclasses import dataclass


@dataclass
class LayerConfiguration:
    name: str
    layer_type: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class MapConfiguration:
    width: int
    height: int
    name: str
    layer_configurations: List[LayerConfiguration]
