import json
import os
import pytest

from mapgen.data.errors import UnknownLayerGeneratorException
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'test_layer',
        'test_generator',
        {
            "type": "int"
        }
   )

@pytest.fixture
def test_layer_configuration_loader():
    return LayerConfigurationLoader()

@pytest.fixture
def test_tile_attribute_accessor():
    def accessor(tile_layer_coordinate):
        return None

    return accessor

@pytest.fixture
def test_map_context():
    return MapContext(f"{ROOT_DIR}/test/resources/data")

def test_layer_configuration_loader_test_generator(test_layer_configuration, test_map_context, test_layer_configuration_loader, test_tile_attribute_accessor):
    layer = test_layer_configuration_loader.load(test_layer_configuration, test_map_context)

    assert layer.name == 'test_layer'

    fn = layer.fn

    assert fn(0, 1, test_tile_attribute_accessor) == 1
    assert fn(5, 15, test_tile_attribute_accessor) == 20
