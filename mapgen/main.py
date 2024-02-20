import os

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)


ROOT_DIR = os.path.abspath(os.curdir)

map_definition = map_configuration_loader.load(
    f"{ROOT_DIR}/test/resources/data/native_layer_configuration.json"
)

import pdb  # noqa

pdb.set_trace()
