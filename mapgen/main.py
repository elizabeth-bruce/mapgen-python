import os

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

from mapgen.use_cases.map_creator import MapCreator

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)


ROOT_DIR = os.path.abspath(os.curdir)

map_definition = map_configuration_loader.load(
    f"{ROOT_DIR}/examples/full_map/configuration.json"
)


if __name__ == "__main__":
    map_creator = MapCreator()
    new_map = map_creator.create_map(map_definition, 1)
