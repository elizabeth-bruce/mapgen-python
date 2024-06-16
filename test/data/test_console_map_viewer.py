import os
import pytest

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader

from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.use_cases.map_creator import MapCreator

from mapgen.data.models import ViewConfiguration, ViewConfigurationSet
from mapgen.data.console_map_viewer import ConsoleMapViewer
from mapgen.data.file_view_configuration_set_loader import FileViewConfigurationSetLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH =  f'{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/configuration.json'
VIEW_PATH = f'{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/views.json'

@pytest.fixture
def file_view_configuration_set_loader():
    return FileViewConfigurationSetLoader(VIEW_PATH)

@pytest.fixture
def view_configuration_set(file_view_configuration_set_loader):
    return file_view_configuration_set_loader.load()

@pytest.fixture
def view_set_context(file_view_configuration_set_loader):
    return file_view_configuration_set_loader.load_view_set_context()

@pytest.fixture
def console_map_viewer(view_configuration_set, view_set_context):
    return ConsoleMapViewer(
        view_configuration_set,
        view_set_context
    )

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

def test_console_map_viewer_happy_path(console_map_viewer, new_map):
    render_str = console_map_viewer.render(new_map, "temperature")
    expected_render_str = '\n'.join(['\x1b[31m@\x1b[0m' * 10] * 10)

    assert render_str == expected_render_str
