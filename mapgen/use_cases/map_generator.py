from mapgen.models import MapDefinition, Map, Tile, TileSet


class MapGenerator:
    def generate_tiles(self, map_definition: MapDefinition) -> TileSet:
        layer = map_definition.layers[0]
        mock_tile = Tile(0, 0, layer, "test")
        mock_tileset = {(0, 0, "foo"): mock_tile}

        return mock_tileset

    def generate_map(self, map_definition: MapDefinition) -> Map:
        return Map(
            map_definition=map_definition,
            tiles=self.generate_tiles(map_definition),
        )
