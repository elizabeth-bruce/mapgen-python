import os
import pytest

from unittest.mock import Mock

from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.use_cases.exceptions import InvalidMapCoordinateException
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader
from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.use_cases.map_creator_process import MapCreatorProcess
from mapgen.use_cases.exceptions import CircularDependencyException

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f"{ROOT_DIR}/test/resources/data/maps/example_map/configuration.json"
MAP_PATH_CIRCULAR_DEPENDENCY = f"{ROOT_DIR}/test/resources/data/maps/circular_dependency_map/configuration.json"

@pytest.fixture
def test_layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def test_map_configuration_loader():
    return FileMapConfigurationLoader(MAP_PATH)

@pytest.fixture
def test_map_configuration_loader_circular_dependency():
    return FileMapConfigurationLoader(MAP_PATH_CIRCULAR_DEPENDENCY)

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
def test_map_definition_loader_circular_dependency(
    test_layer_configuration_loader,
    test_map_configuration_loader_circular_dependency
):
    return MapDefinitionLoader(
        test_layer_configuration_loader,
        test_map_configuration_loader_circular_dependency
    )

@pytest.fixture
def map_definition(test_map_definition_loader):
    return test_map_definition_loader.load()

@pytest.fixture
def map_definition_circular_dependency(test_map_definition_loader_circular_dependency):
    return test_map_definition_loader_circular_dependency.load()

@pytest.fixture
def map_accessor(map_definition):
     return SharedMemoryMapAccessor(map_definition)

@pytest.fixture
def map_accessor_circular_dependency(map_definition_circular_dependency):
     map_accessor = SharedMemoryMapAccessor(map_definition_circular_dependency)
     return map_accessor

@pytest.fixture
def layer_fn_map(map_definition):
    layer_fn_map = {
        layer.name: layer.fn for layer in map_definition.layers
    }

    return layer_fn_map

@pytest.fixture
def layer_fn_map_circular_dependency(map_definition_circular_dependency):
    layer_fn_map = {
        layer.name: layer.fn for layer in map_definition_circular_dependency.layers
    }

    return layer_fn_map

def test_map_creator_process_process_map_coordinates(map_accessor, layer_fn_map):
    map_creator_process = MapCreatorProcess(map_accessor, layer_fn_map, Mock())

    map_coordinates = [(0, 0, 'base'), (0, 0, 'dependent')]
    map_creator_process.process_map_coordinates(map_coordinates)

    assert map_accessor[(0, 0, 'base')] == 0
    assert map_accessor[(0, 0, 'dependent')] == -1

def test_map_creator_process_circular_dependency(map_accessor_circular_dependency, layer_fn_map_circular_dependency):
    map_creator_process = MapCreatorProcess(map_accessor_circular_dependency, layer_fn_map_circular_dependency, Mock())

    map_coordinates = [(0, 0, 'base'), (0, 0, 'dependent')]

    with pytest.raises(CircularDependencyException):
        map_creator_process.process_map_coordinates(map_coordinates)
