import json
import os
import pytest

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.native_layer_generator import NativeLayerGenerator

ROOT_DIR = os.path.abspath(os.curdir)


@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'example',
        'native_generator',
        {
            "type": "int",
            "filename": "example_layer_fn.py"
        }
   )

@pytest.fixture
def native_layer_generator():
    return NativeLayerGenerator()

@pytest.fixture
def test_tile_attribute_accessor():
    def accessor(tile_layer_coordinate):
        return None

@pytest.fixture
def test_map_context():
    return MapContext(f"{ROOT_DIR}/test/resources/data")

def test_native_layer_generator_resolve(test_layer_configuration, test_map_context, native_layer_generator, test_tile_attribute_accessor):
    layer = native_layer_generator.resolve(test_layer_configuration, test_map_context)

    assert layer.name == 'example'

    fn = layer.fn

    assert fn(0, 1, test_tile_attribute_accessor) == 0
    assert fn(5, 15, test_tile_attribute_accessor) == 75
