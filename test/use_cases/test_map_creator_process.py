import os
import pytest

from unittest.mock import Mock

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.exceptions import InvalidMapCoordinateException
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

ROOT_DIR = os.path.abspath(os.curdir)

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)

from mapgen.use_cases.map_creator_process import MapCreatorProcess

@pytest.fixture
def map_definition():
    map_definition = map_configuration_loader.load(
        f"{ROOT_DIR}/test/resources/data/maps/example_map/configuration.json"
    )

    return map_definition

@pytest.fixture
def map_accessor(map_definition):
     map_accessor = SharedMemoryMapAccessor(map_definition)
     return map_accessor

@pytest.fixture
def layer_fn_map(map_definition):
    layer_fn_map = {
        layer.name: layer.fn for layer in map_definition.layers
    }

    return layer_fn_map

def test_map_creator_process_process_map_coordinates(map_accessor, layer_fn_map):
    map_creator_process = MapCreatorProcess(map_accessor, layer_fn_map, Mock())

    map_coordinates = [(0, 0, 'base'), (0, 0, 'dependent')]
    map_creator_process.process_map_coordinates(map_coordinates)

    assert map_accessor[(0, 0, 'base')] == 0
    assert map_accessor[(0, 0, 'dependent')] == -1
