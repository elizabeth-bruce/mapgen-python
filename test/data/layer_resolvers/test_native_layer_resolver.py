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
    async def accessor(x, y, layer):
        return None

@pytest.fixture
def test_map_context():
    return MapContext(f"{ROOT_DIR}/test/resources/data")

@pytest.mark.asyncio
async def test_native_layer_resolver_resolve(test_layer_configuration, test_map_context, native_layer_resolver, test_tile_attribute_accessor):
    layer = native_layer_resolver.resolve(test_layer_configuration, test_map_context)

    assert layer.name == 'example'

    fn = layer.fn

    assert await fn(0, 1, test_tile_attribute_accessor) == 0
    assert await fn(5, 15, test_tile_attribute_accessor) == 75
