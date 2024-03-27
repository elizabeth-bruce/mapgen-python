import json
import os
import pytest

from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.lua_layer_generator import LuaLayerGenerator

ROOT_DIR = os.path.abspath(os.curdir)


@pytest.fixture
def test_layer_configuration():
    return LayerConfiguration(
        'base',
        'LUA',
        {
            "type": "int",
            "filename": "base.lua"
        }
   )

@pytest.fixture
def lua_layer_generator():
    return LuaLayerGenerator()

@pytest.fixture
def test_tile_attribute_accessor():
    def accessor(tile_layer_coordinate):
        return None

@pytest.fixture
def test_map_context():
    return MapContext(f"{ROOT_DIR}/test/resources/data/maps/lua_map")

def test_lua_layer_generator_resolve(test_layer_configuration, test_map_context, lua_layer_generator, test_tile_attribute_accessor):
    layer = lua_layer_generator.resolve(test_layer_configuration, test_map_context)

    assert layer.name == 'base'

    fn = layer.fn

    assert fn(0, 1, test_tile_attribute_accessor) == 0
    assert fn(5, 15, test_tile_attribute_accessor) == 75
