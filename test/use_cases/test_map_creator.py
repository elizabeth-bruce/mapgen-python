import os
import pytest

from mapgen.use_cases.map_creator import MapCreator
from mapgen.models import Layer, Map, MapDefinition

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.map_configuration_loader import MapConfigurationLoader

layer_configuration_loader = LayerConfigurationLoader()
map_configuration_loader = MapConfigurationLoader(layer_configuration_loader)


ROOT_DIR = os.path.abspath(os.curdir)

@pytest.fixture
def map_definition():
    map_definition = map_configuration_loader.load(
        f"{ROOT_DIR}/test/resources/data/maps/example_map/configuration.json"
    )

    return map_definition

@pytest.fixture
def map_creator():
    return MapCreator()

@pytest.mark.asyncio
async def test_generate_map(map_definition, map_creator):
    expected_map = Map(
        map_definition = map_definition,
        map_coordinates = {
            (0, 0, "base"): 0,
            (0, 0, "dependent"): -1
        }
    )


    actual_map = await map_creator.create_map(map_definition)

    assert expected_map == actual_map
