import json
import os
import pytest

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_resolvers.native_layer_resolver import NativeLayerResolver

ROOT_DIR = os.path.abspath(os.curdir)


@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'example',
        'int',
        'native_resolver',
        {
            "filename": "example_layer_fn.py"
        }
   )

@pytest.fixture
def native_layer_resolver():
    return NativeLayerResolver()

@pytest.fixture
def test_tile_attribute_accessor():
    def accessor(tile_layer_coordinate):
        return None

@pytest.fixture
def test_map_context():
    return MapContext(f"{ROOT_DIR}/test/resources/data")

def test_native_layer_resolver_resolve(test_layer_configuration, test_map_context, native_layer_resolver, test_tile_attribute_accessor):
    layer = native_layer_resolver.resolve(test_layer_configuration, test_map_context)

    assert layer.name == 'example'

    fn = layer.fn

    assert fn(0, 1, test_tile_attribute_accessor) == 0
    assert fn(5, 15, test_tile_attribute_accessor) == 75
