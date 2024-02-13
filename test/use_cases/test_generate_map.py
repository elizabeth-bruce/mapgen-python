import pytest

from mapgen.use_cases.generate_map import generate_map
from mapgen.models import Layer, Map, MapDefinition, Tile

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

def test_generate_map(map_definition):
    expected_map = Map(
        map_definition = map_definition,
        tiles = {
            (0, 0, "foo"): Tile(
                0, 0,
                map_definition.layers[0],
               'test'
            )
        }
    )


    actual_map = generate_map(map_definition)

    assert expected_map == actual_map
