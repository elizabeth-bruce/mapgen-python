import json
import os

from mapgen.models import MapDefinition
from mapgen.data.models import LayerConfiguration, MapConfiguration, MapContext

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader


class MapConfigurationLoader:
    def __init__(self, layer_configuration_loader: LayerConfigurationLoader):
        self.layer_configuration_loader = layer_configuration_loader

    def __generate_map_context(self, filename: str) -> MapContext:
        map_file_path = os.path.dirname(filename)
        map_context = MapContext(map_file_path)

        return map_context

    def __load_file(self, filename: str) -> MapConfiguration:
        try:
            with open(filename, "r") as config_file:
                config_json = json.load(config_file)
                layer_configurations = [
                    LayerConfiguration(**layer_configuration)
                    for layer_configuration in config_json[
                        "layer_configurations"
                    ]
                ]

                config_json["layer_configurations"] = layer_configurations
                map_configuration = MapConfiguration(**config_json)

                return map_configuration
        except Exception as err:
            # TODO: Add logging support
            print(f"Error while loading file: {err}")
            raise err

    def __generate_map_definition(
        self, map_configuration: MapConfiguration, map_context: MapContext
    ) -> MapDefinition:
        layers = [
            self.layer_configuration_loader.load(
                layer_configuration, map_context
            )
            for layer_configuration in map_configuration.layer_configurations
        ]

        map_definition = MapDefinition(
            map_configuration.name,
            map_configuration.width,
            map_configuration.height,
            layers,
        )

        return map_definition

    def load(self, filename: str) -> MapDefinition:
        map_configuration = self.__load_file(filename)
        map_context = self.__generate_map_context(filename)
        map_definition = self.__generate_map_definition(
            map_configuration, map_context
        )

        return map_definition
