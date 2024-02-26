import os

import cProfile

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

from mapgen.use_cases.map_creator import MapCreator

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)


ROOT_DIR = os.path.abspath(os.curdir)

map_definition = map_configuration_loader.load(
    f"{ROOT_DIR}/test/resources/data/maps/dependent_layers/configuration.json"
)

map_creator = MapCreator()

# map_coordinate_set = asyncio.run(map_creator.create_map(map_definition))
cProfile.run("map_coordinate_set = map_creator.create_map(map_definition)")

import pdb  # noqa

pdb.set_trace()
