import lupa.luajit20 as lupa
import os

from typing import Any

from mapgen.models import UserDefinedFnLayer, TileAttributeAccessor
from mapgen.data.models import LayerConfiguration, MapContext
from mapgen.data.layer_generators.layer_generator import LayerGenerator

LUA_GET_ATTRIBUTE_VALUE_SETTER = """
function set_get_attribute_value(fn)
    rawset(_G, 'get_attribute_value', fn)
end
"""

LUA_CONSTRUCT_MAP_COORDINATE_SETTER = """
function set_construct_map_coordinate(map_coordinate_constructor)
    rawset(_G, 'construct_map_coordinate', map_coordinate_constructor)
end
"""

LUA_GET_TILE_FN = """
Tile = {}
Tile.mt = {}

Tile.mt.__index = function(table, key)
    if key == "x" or key == "y" then
        return rawget(table, key)
    else
        map_coordinate = construct_map_coordinate(rawget(table, "x"), rawget(table, "y"), key)
        return get_attribute_value(map_coordinate)
    end
end

function Tile.new(x, y)
    t = {x=x, y=y}
    setmetatable(t, Tile.mt)

    return t
end

function get_tile(x, y)
    return Tile.new(x, y)
end

"""


class LuaLayerGenerator(LayerGenerator):
    def resolve(
        self, layer_configuration: LayerConfiguration, map_context: MapContext
    ) -> UserDefinedFnLayer:
        layer_context = layer_configuration.context
        lua = lupa.LuaRuntime(register_eval=False, unpack_returned_tuples=False)

        lua.execute(LUA_GET_ATTRIBUTE_VALUE_SETTER)
        lua_set_get_attribute_value = lua.globals().set_get_attribute_value

        lua.execute(LUA_CONSTRUCT_MAP_COORDINATE_SETTER)
        lua_set_construct_map_coordinate = lua.globals().set_construct_map_coordinate

        lua_set_construct_map_coordinate(
            lambda x, y, layer: (
                x,
                y,
                layer,
            )
        )

        file_path = os.path.join(map_context.file_path, layer_context["filename"])

        lua.execute(LUA_GET_TILE_FN)
        with open(file_path, "r") as lua_file:
            lua.execute(lua_file.read())

        lua_globals = lua.globals()
        lua_fn = getattr(lua_globals, layer_configuration.name)
        assert lua_fn is not None, f"Lua function {layer_configuration.name} not found!"

        def layer_fn(x: int, y: int, accessor: TileAttributeAccessor) -> Any:
            lua_set_get_attribute_value(accessor)
            return lua_fn(x, y)

        layer = UserDefinedFnLayer(
            name=layer_configuration.name,
            type=layer_configuration.context["type"],
            fn=layer_fn,
        )

        return layer
