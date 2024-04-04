import os
import pytest

from mapgen.use_cases.map_creator import MapCreator
from mapgen.models import Layer, LayerMetadata, Map, MapDefinition, MapMetadata

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
def test_map_definition(test_map_definition_loader):
    return test_map_definition_loader.load()

@pytest.fixture
def test_map_creator():
    return MapCreator()

@pytest.fixture
def test_map_metadata():
    return MapMetadata(
        name="example_map",
        width=1,
        height=1,
        layers=[
            LayerMetadata(
                name="base",
                type="int"
            ),
            LayerMetadata(
                name="dependent",
                type="int"
            )
        ]
    )

@pytest.fixture
def seed():
    return 1

def test_generate_map(test_map_definition, test_map_metadata, test_map_creator, seed):
    actual_map = test_map_creator.create_map(test_map_definition, seed)

    assert actual_map.map_metadata == test_map_metadata

    assert actual_map.map_accessor[(0, 0, 'base')] == 0
    assert actual_map.map_accessor[(0, 0, 'dependent')] == -1
