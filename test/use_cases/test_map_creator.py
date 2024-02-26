import pytest

from mapgen.use_cases.map_creator import MapCreator
from mapgen.models import Layer, Map, MapDefinition

@pytest.fixture
def map_definition():
    async def test_layer_fn(x: int, y: int, accessor):
        return "test"

    layer = Layer(
        'foo',
        test_layer_fn
    )

    return MapDefinition(
        'test_definition',
        1,
        1,
        [layer]
    )

@pytest.fixture
def map_creator():
    return MapCreator()

@pytest.mark.asyncio
async def test_generate_map(map_definition, map_creator):
    expected_map = Map(
        map_definition = map_definition,
        map_coordinates = {
            (0, 0, "foo"): 'test'
        }
    )


    actual_map = await map_creator.create_map(map_definition)

    assert expected_map == actual_map
