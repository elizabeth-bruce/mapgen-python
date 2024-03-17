import json
import os
import pytest

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.test_layer_generator import TestLayerGenerator

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
def test_layer_generator():
    return TestLayerGenerator()

@pytest.fixture
def test_tile_attribute_accessor():
    async def accessor(tile_layer_coordinate):
        return None

@pytest.fixture
def test_map_context():
    return MapContext("")

def test_test_layer_generator_resolve(test_layer_configuration, test_map_context, test_layer_generator, test_tile_attribute_accessor):
    layer = test_layer_generator.resolve(test_layer_configuration, test_map_context)

    assert layer.name == 'test_layer'

    fn = layer.fn

    assert fn(0, 1, test_tile_attribute_accessor) == 1
    assert fn(5, 15, test_tile_attribute_accessor) == 20
