import pytest

from mapgen.use_cases.map_generator import MapGenerator
from mapgen.models import Layer, Map, MapDefinition

@pytest.fixture
def map_definition():
    async def test_layer_fn(x: int, y: int):
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
def map_generator():
    return MapGenerator()

def test_generate_map(map_definition, map_generator):
    expected_map = Map(
        map_definition = map_definition,
        tiles = {
            (0, 0, "foo"): 'test'
        }
    )


    actual_map = map_generator.generate_map(map_definition)

    assert expected_map == actual_map
