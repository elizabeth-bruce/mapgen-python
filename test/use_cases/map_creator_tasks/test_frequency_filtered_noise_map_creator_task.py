import os
import pytest

from numpy.random import RandomState

from mapgen.use_cases.map_creator_tasks.frequency_filtered_noise_map_creator_task import (
    FrequencyFilteredNoiseMapCreatorTask
)

from mapgen.models import MapDefinition
from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader
from mapgen.data.map_definition_loader import MapDefinitionLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f'{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/configuration.json'

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
    map_definition = test_map_definition_loader.load()

    return map_definition

@pytest.fixture
def random_state():
    return RandomState(1)

@pytest.fixture
def test_shared_memory_map_accessor(test_map_definition):
    return SharedMemoryMapAccessor(test_map_definition)

@pytest.fixture
def test_map_creator_task(test_shared_memory_map_accessor):
    return FrequencyFilteredNoiseMapCreatorTask(test_shared_memory_map_accessor)


def test_frequency_filtered_noise_map_creator_task_populate(test_map_creator_task, test_map_definition, random_state):
    test_map_creator_task.populate(test_map_definition, random_state)

    assert 5.265 < test_map_creator_task.map_accessor[0, 0, 'base'] < 5.266
