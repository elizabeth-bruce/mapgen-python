import json
import os
import pytest

from mapgen.data.models import LayerConfiguration
from mapgen.data.layer_resolvers.test_layer_resolver import TestLayerResolver

@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'test_layer',
        'test_resolver'
   )

@pytest.fixture
def test_layer_resolver():
    return TestLayerResolver()

@pytest.fixture
def test_tile_attribute_accessor():
    async def accessor(x, y, layer):
        return None

@pytest.mark.asyncio
async def test_test_layer_resolver_resolve(test_layer_configuration, test_layer_resolver, test_tile_attribute_accessor):
    layer = test_layer_resolver.resolve(test_layer_configuration)

    assert layer.name == 'test_layer'

    fn = layer.fn

    assert await fn(0, 1, test_tile_attribute_accessor) == 1
    assert await fn(5, 15, test_tile_attribute_accessor) == 20
