import os

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader

from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.data.file_view_configuration_set_loader import FileViewConfigurationSetLoader
from mapgen.data.console_map_viewer import ConsoleMapViewer

from mapgen.use_cases.map_creator import MapCreator

from mapgen.data.compressed_npz_map_saver import CompressedNpzMapSaver
from mapgen.data.compressed_npz_map_loader import CompressedNpzMapLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f"{ROOT_DIR}/examples/full_map/configuration.json"
VIEW_PATH = f"{ROOT_DIR}/examples/full_map/views.json"

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = FileMapConfigurationLoader(MAP_PATH)

map_definition_loader = MapDefinitionLoader(layer_configuration_loader, map_configuration_loader)

map_configuration = map_configuration_loader.load_map_configuration()
map_context = map_configuration_loader.load_map_context()
map_definition = map_definition_loader.load()

map_saver = CompressedNpzMapSaver()
map_loader = CompressedNpzMapLoader()

view_configuration_set_loader = FileViewConfigurationSetLoader(VIEW_PATH)

if __name__ == "__main__":
    map_creator = MapCreator()
    new_map = map_creator.create_map(map_definition, 914)

    view_configuration_set = view_configuration_set_loader.load()
    view_set_context = view_configuration_set_loader.load_view_set_context()

    console_map_viewer = ConsoleMapViewer(view_configuration_set, view_set_context)

    render_str = console_map_viewer.render(new_map, "height")
    print(render_str)
