import numpy as np

import json

from numpy.typing import NDArray

from mapgen.models import LayerMetadata, Map, MapMetadata
from mapgen.use_cases.shared_memory_map_accessor import SharedMemoryMapAccessor

from mapgen.data.map_loader import MapLoader

MAP_METADATA_KEY = "__METADATA"
METADATA_ENCODING = "utf-8"


class CompressedNpzMapLoader(MapLoader):
    def load(self, path: str) -> Map:
        layer_raw_values = np.load(path)

        map_metadata = self.__deserialize_map_metadata(layer_raw_values[MAP_METADATA_KEY])

        map_accessor = SharedMemoryMapAccessor(map_metadata)

        layer_names = [layer.name for layer in map_metadata.layers]

        for layer_name in layer_names:
            self.__populate_shared_memory(map_accessor, layer_name, layer_raw_values[layer_name])

        new_map = Map(map_metadata, map_accessor)

        return new_map

    def __populate_shared_memory(
        self, map_accessor: SharedMemoryMapAccessor, layer_name: str, array: NDArray
    ) -> None:
        shared_memory = map_accessor.get_shared_memory(layer_name)
        destination: NDArray = np.ndarray(
            shape=(map_accessor.height * map_accessor.width),
            dtype=array.dtype,
            buffer=shared_memory,
        )

        np.copyto(destination, array)

    def __deserialize_map_metadata(self, configuration_array: NDArray) -> MapMetadata:
        metadata_bytes = configuration_array.tobytes()
        metadata_str = metadata_bytes.decode(METADATA_ENCODING)

        metadata_dict = json.loads(metadata_str)

        # Hack to quickly deserialize layers without having to define
        # a nested parser hierarchy
        metadata_dict["layers"] = [LayerMetadata(**layer) for layer in metadata_dict["layers"]]
        map_metadata = MapMetadata(**metadata_dict)

        return map_metadata
