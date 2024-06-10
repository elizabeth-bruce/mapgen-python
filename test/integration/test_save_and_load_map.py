import os
from pathlib import Path
import pytest

from numpy import array_equal

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader

from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.use_cases.map_creator import MapCreator

from mapgen.data.compressed_npz_map_saver import CompressedNpzMapSaver
from mapgen.data.compressed_npz_map_loader import CompressedNpzMapLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f"{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/configuration.json"

@pytest.fixture
def layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def map_configuration_loader():
    return FileMapConfigurationLoader(MAP_PATH)

@pytest.fixture
def map_definition_loader(layer_configuration_loader, map_configuration_loader):
    return MapDefinitionLoader(layer_configuration_loader, map_configuration_loader)

@pytest.fixture
def map_configuration(map_configuration_loader):
    return map_configuration_loader.load_map_configuration()

@pytest.fixture
def map_context(map_configuration_loader):
    return map_configuration_loader.load_map_context()

@pytest.fixture
def map_definition(map_definition_loader):
    return map_definition_loader.load()

@pytest.fixture()
def new_map(map_definition):
    map_creator = MapCreator()
    return map_creator.create_map(map_definition, 1)

@pytest.fixture
def map_saver():
    return CompressedNpzMapSaver()

@pytest.fixture
def map_loader():
    return CompressedNpzMapLoader()

@pytest.fixture(autouse=True)
def cleanup(request):
    TEST_MAP_FILE_PATH = f"{ROOT_DIR}/test/resources/data/test_map.npz"
    def remove_test_map_file():
        Path.unlink(TEST_MAP_FILE_PATH)
    request.addfinalizer(remove_test_map_file)

def test_integration_save_load_map(map_saver, map_loader, new_map):
    TEST_MAP_FILE_PATH = f"{ROOT_DIR}/test/resources/data/test_map.npz"

    map_saver.save(new_map, TEST_MAP_FILE_PATH)
    loaded_map = map_loader.load(TEST_MAP_FILE_PATH)

    assert new_map.map_metadata == loaded_map.map_metadata

    layer_names = [
        layer.name
        for layer in new_map.map_metadata.layers
    ]

    for layer_name in layer_names:
        assert array_equal(
            new_map.map_accessor.get_raw_values(layer_name),
            loaded_map.map_accessor.get_raw_values(layer_name)
        )
