from mapgen.models import MapDefinition, Map, TileSet


class MapGenerator:
    def __init__(self):
        self.priority_tile_attributes = []
        self.current_tile_layer_coordinate = None

    def generate_tiles(self, map_definition: MapDefinition) -> TileSet:
        mock_tileset = {(0, 0, "foo"): "test"}

        return mock_tileset

    def generate_map(self, map_definition: MapDefinition) -> Map:
        return Map(
            map_definition=map_definition,
            tiles=self.generate_tiles(map_definition),
        )
