import lupa.luajit20 as lupa
import os

from typing import Any, Callable, Dict

from mapgen.models import Map

from mapgen.use_cases.map_viewer import MapViewer
from mapgen.data.models import ViewConfiguration, ViewConfigurationSet, ViewSetContext

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


class ConsoleMapViewer(MapViewer[str]):
    VIEW_CONFIGURATION_KEY = "CONSOLE"

    view_fn_map: Dict[str, Callable[[int, int], Any]]

    def __init__(
        self, view_configuration_set: ViewConfigurationSet, view_set_context: ViewSetContext
    ):
        self.view_set_context = view_set_context
        view_configurations = view_configuration_set.view_configurations

        console_view_configurations = [
            view_configuration
            for view_configuration in view_configurations
            if view_configuration.type == ConsoleMapViewer.VIEW_CONFIGURATION_KEY
        ]

        self.lua = lupa.LuaRuntime(register_eval=False, unpack_returned_tuples=False)

        self.lua.execute(LUA_GET_ATTRIBUTE_VALUE_SETTER)

        self.lua.execute(LUA_CONSTRUCT_MAP_COORDINATE_SETTER)
        lua_set_construct_map_coordinate = self.lua.globals().set_construct_map_coordinate

        lua_set_construct_map_coordinate(
            lambda x, y, layer: (
                x,
                y,
                layer,
            )
        )

        self.view_render_fn_map = {}
        for configuration in console_view_configurations:
            self.view_render_fn_map[configuration.name] = self.get_view_render_fn(configuration)

    def get_view_render_fn(
        self, view_configuration: ViewConfiguration
    ) -> Callable[[int, int], Any]:
        view_context = view_configuration.context
        file_path = os.path.join(self.view_set_context.file_path, view_context["filename"])

        self.lua.execute(LUA_GET_TILE_FN)
        with open(file_path, "r") as lua_file:
            self.lua.execute(lua_file.read())

        lua_globals = self.lua.globals()
        lua_fn = getattr(lua_globals, view_configuration.name)
        assert lua_fn is not None, f"Lua function {view_configuration.name} not found!"

        return lua_fn

    def render(self, target_map: Map, view: str = "default") -> str:
        def tile_attribute_accessor(map_coordinate):
            return target_map.map_accessor[map_coordinate]

        lua_set_get_attribute_value = self.lua.globals().set_get_attribute_value
        lua_set_get_attribute_value(tile_attribute_accessor)

        tile_coordinates_list = [
            (x, y)
            for y in range(target_map.map_metadata.height)
            for x in range(target_map.map_metadata.width)
        ]

        render_str = ""

        render_fn = self.view_render_fn_map[view]

        for coordinate in tile_coordinates_list:
            render_str += render_fn(*coordinate)
            if (
                coordinate[0] == target_map.map_metadata.width - 1
                and coordinate[1] < target_map.map_metadata.height - 1
            ):
                render_str += "\n"

        return render_str
