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

@pytest.mark.asyncio
async def test_test_layer_resolver_resolve(test_layer_configuration, test_layer_resolver):
    layer = test_layer_resolver.resolve(test_layer_configuration)

    assert layer.name == 'test_layer'

    fn = layer.fn

    assert await fn(0, 1) == 1
    assert await fn(5, 15) == 20
