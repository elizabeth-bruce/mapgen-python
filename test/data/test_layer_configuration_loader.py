import json
import os
import pytest

from mapgen.data.errors import UnknownLayerResolverException
from mapgen.data.models import LayerConfiguration
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'test_layer',
        'test_resolver'
   )

@pytest.fixture
def test_layer_configuration_unknown_layer_type():
    return LayerConfiguration(
        'test_layer',
        'unknown_resolver'
    )

@pytest.fixture
def test_layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def test_tile_attribute_accessor():
    async def accessor(x, y, layer):
        return None

@pytest.mark.asyncio
async def test_layer_configuration_loader_test_resolver(test_layer_configuration, test_layer_configuration_loader, test_tile_attribute_accessor):
    layer = test_layer_configuration_loader.load(test_layer_configuration)

    assert layer.name == 'test_layer'

    fn = layer.fn

    assert await fn(0, 1, test_tile_attribute_accessor) == 1
    assert await fn(5, 15, test_tile_attribute_accessor) == 20

def test_layer_configuration_loader_unknown_layer_type(test_layer_configuration_unknown_layer_type, test_layer_configuration_loader):
    with pytest.raises(UnknownLayerResolverException) as exc:
        test_layer_configuration_loader.load(test_layer_configuration_unknown_layer_type)

