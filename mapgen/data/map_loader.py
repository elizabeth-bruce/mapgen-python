from typing import Tuple

import numpy as np

import json
import os

from abc import ABC, abstractmethod

from mapgen.models import Map, MapDefinition
from mapgen.data.models import MapConfiguration


class MapLoader(ABC):
    @abstractmethod
    def load(path: str) -> Tuple[Map, MapConfiguration]:
        pass
