import numpy as np

import dataclasses
import json

from numpy.typing import NDArray

from mapgen.models import Map, MapMetadata
from mapgen.data.map_saver import MapSaver

MAP_METADATA_KEY = "__METADATA"


class CompressedNpzMapSaver(MapSaver):
    def save(
        self,
        save_map: Map,
        filename: str,
    ) -> None:
        map_metadata = save_map.map_metadata
        layer_names = [layer.name for layer in map_metadata.layers]

        save_kw_arguments = {
            layer_name: save_map.map_accessor.get_raw_values(layer_name)
            for layer_name in layer_names
        }

        map_metadata_array = self.__serialize_map_metadata(map_metadata)
        save_kw_arguments[MAP_METADATA_KEY] = map_metadata_array

        np.savez_compressed(filename, **save_kw_arguments)

    def __serialize_map_metadata(self, map_metadata: MapMetadata) -> NDArray:
        metadata_str = json.dumps(dataclasses.asdict(map_metadata))

        metadata_array = np.fromstring(string=metadata_str, dtype="S1")  # type: ignore

        return metadata_array
