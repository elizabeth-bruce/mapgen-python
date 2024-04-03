import numpy as np

import json
import os

from abc import ABC, abstractmethod

from mapgen.models import Map, MapDefinition
from mapgen.data.models import MapConfiguration


class MapSaver(ABC):
    @abstractmethod
    def save(save_map: Map, map_configuration: MapConfiguration, path: str) -> None:
        pass
