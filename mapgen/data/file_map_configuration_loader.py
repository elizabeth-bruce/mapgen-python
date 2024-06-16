import json
import os

from mapgen.data.models import LayerConfiguration, MapConfiguration, MapContext

from mapgen.data.map_configuration_loader import MapConfigurationLoader


class FileMapConfigurationLoader(MapConfigurationLoader):
    def __init__(self, filename: str):
        self.filename = filename

    def load_map_configuration(self) -> MapConfiguration:
        try:
            with open(self.filename, "r") as config_file:
                config_dict = json.load(config_file)
                layer_configurations = [
                    LayerConfiguration(**layer_configuration)
                    for layer_configuration in config_dict["layer_configurations"]
                ]

                config_dict["layer_configurations"] = layer_configurations
                map_configuration = MapConfiguration(**config_dict)

                return map_configuration
        except Exception as err:
            # TODO: Add logging support
            print(f"Error while loading file: {err}")
            raise err

    def load_map_context(self) -> MapContext:
        map_file_path = os.path.dirname(self.filename)
        map_context = MapContext(map_file_path)

        return map_context
