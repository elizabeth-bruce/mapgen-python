import os
import pytest

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.exceptions import InvalidMapCoordinateException
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)

ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture
def map_definition():
    map_definition = map_configuration_loader.load(
        f"{ROOT_DIR}/test/resources/data/maps/example_map/configuration.json"
    )

    return map_definition

def test_shared_memory_map_accessor(map_definition):
    map_accessor = SharedMemoryMapAccessor(map_definition)

    map_coordinate = (0, 0, 'base')
    assert map_accessor[map_coordinate] == 0

    map_accessor[map_coordinate] = 15

    assert map_accessor[map_coordinate] == 15

def test_shared_memory_map_accessor_invalid_layer(map_definition):
    map_accessor = SharedMemoryMapAccessor(map_definition)

    map_coordinate = (0, 0, 'invalid_layer')

    with pytest.raises(InvalidMapCoordinateException):
        map_accessor[map_coordinate]

def test_shared_memory_map_accessor_invalid_coordinate(map_definition):
    map_accessor = SharedMemoryMapAccessor(map_definition)

    map_coordinate = (-1, 0, 'base')

    with pytest.raises(InvalidMapCoordinateException):
        map_accessor[map_coordinate]

    map_coordinate = (0, 99999, 'base')

    with pytest.raises(InvalidMapCoordinateException):
        map_accessor[map_coordinate]

