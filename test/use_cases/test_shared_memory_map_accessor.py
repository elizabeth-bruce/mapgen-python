import os
import pytest

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.exceptions import InvalidMapCoordinateException
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader
from mapgen.data.map_definition_loader import MapDefinitionLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f"{ROOT_DIR}/test/resources/data/maps/example_map/configuration.json"

@pytest.fixture
def test_layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def test_map_configuration_loader():
    return FileMapConfigurationLoader(MAP_PATH)

@pytest.fixture
def test_map_definition_loader(
    test_layer_configuration_loader,
    test_map_configuration_loader
):
    return MapDefinitionLoader(
        test_layer_configuration_loader,
        test_map_configuration_loader
    )

@pytest.fixture
def map_definition(test_map_definition_loader):
    return test_map_definition_loader.load()

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

