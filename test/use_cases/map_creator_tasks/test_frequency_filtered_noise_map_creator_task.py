import os
import pytest

from numpy.random import RandomState

from mapgen.use_cases.map_creator_tasks.frequency_filtered_noise_map_creator_task import (
    FrequencyFilteredNoiseMapCreatorTask
)

from mapgen.models import MapDefinition
from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture
def layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def map_configuration_loader(layer_configuration_loader):
    return MapConfigurationLoader(layer_configuration_loader)

@pytest.fixture
def map_definition(map_configuration_loader):
    map_definition = map_configuration_loader.load(
        f"{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/configuration.json"
    )

    return map_definition

@pytest.fixture
def random_state():
    return RandomState(1)

@pytest.fixture
def shared_memory_map_accessor(map_definition):
    return SharedMemoryMapAccessor(map_definition)

@pytest.fixture
def map_creator_task(shared_memory_map_accessor):
    return FrequencyFilteredNoiseMapCreatorTask(shared_memory_map_accessor)


def test_frequency_filtered_noise_map_creator_task_populate(map_creator_task, map_definition, random_state):
    map_creator_task.populate(map_definition, random_state)

    assert 5.265 < map_creator_task.map_accessor[0, 0, 'base'] < 5.266
