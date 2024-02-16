import json
import os
import pytest

from mapgen.data.models import MapConfiguration
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture
def test_layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def test_map_configuration_loader(test_layer_configuration_loader):
    return MapConfigurationLoader(test_layer_configuration_loader)

@pytest.fixture
def test_tile_attribute_accessor():
    async def accessor(x, y, layer):
        return None

@pytest.mark.asyncio
async def test_map_configuration_loader_happy_path(test_map_configuration_loader, test_tile_attribute_accessor):
    map_definition = test_map_configuration_loader.load(f'{ROOT_DIR}/test/resources/data/example_configuration.json')

    assert map_definition.width == 10
    assert map_definition.height == 10

    assert map_definition.name == 'test_map'

    assert len(map_definition.layers) == 1

    layer = map_definition.layers[0]

    assert layer.name == 'bottom_layer'

    fn = layer.fn

    assert await fn(0, 1, test_tile_attribute_accessor) == 1
    assert await fn(5, 15, test_tile_attribute_accessor) == 20
