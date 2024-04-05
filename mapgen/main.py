import os

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader

from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.use_cases.map_creator import MapCreator

from mapgen.data.compressed_npz_map_saver import CompressedNpzMapSaver
from mapgen.data.compressed_npz_map_loader import CompressedNpzMapLoader

ROOT_DIR = os.path.abspath(os.curdir)
MAP_PATH = f"{ROOT_DIR}/examples/full_map/configuration.json"


layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = FileMapConfigurationLoader(MAP_PATH)

map_definition_loader = MapDefinitionLoader(layer_configuration_loader, map_configuration_loader)

map_configuration = map_configuration_loader.load_map_configuration()
map_context = map_configuration_loader.load_map_context()
map_definition = map_definition_loader.load()

map_saver = CompressedNpzMapSaver()
map_loader = CompressedNpzMapLoader()

if __name__ == "__main__":
    map_creator = MapCreator()
    new_map = map_creator.create_map(map_definition, 1)

    map_saver.save(new_map, "test.npz")
    loaded_map = map_loader.load("test.npz")

    import pdb

    pdb.set_trace()
