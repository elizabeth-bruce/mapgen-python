import os
import pytest

from mapgen.data.models import ViewConfiguration, ViewConfigurationSet
from mapgen.data.file_view_configuration_set_loader import FileViewConfigurationSetLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f'{ROOT_DIR}/test/resources/data/views.json'

@pytest.fixture
def file_view_configuration_set_loader():
    return FileViewConfigurationSetLoader(MAP_PATH)

def test_view_configuration_set_loader_load(file_view_configuration_set_loader):
    view_configuration_set = file_view_configuration_set_loader.load()

    expected_view_configuration_set = ViewConfigurationSet(
        view_configurations = [
            ViewConfiguration(
                name='temperature',
                type='CONSOLE',
                context={
                    "filename": 'view_temperature.lua'
                }
            )
        ]
    )

    assert view_configuration_set == expected_view_configuration_set
