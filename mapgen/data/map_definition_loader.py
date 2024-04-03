import json
import os

from mapgen.models import MapDefinition
from mapgen.data.models import LayerConfiguration, MapConfiguration, MapContext
from mapgen.data.map_configuration_loader import MapConfigurationLoader
from mapgen.data.layer_configuration_loader import LayerConfigurationLoader


class MapDefinitionLoader:
    def __init__(
        self,
        layer_configuration_loader: LayerConfigurationLoader,
        map_configuration_loader: MapConfigurationLoader,
    ):
        self.layer_configuration_loader = layer_configuration_loader
        self.map_configuration_loader = map_configuration_loader

    def __generate_map_definition(
        self, map_configuration: MapConfiguration, map_context: MapContext
    ) -> MapDefinition:
        layers = [
            self.layer_configuration_loader.load(layer_configuration, map_context)
            for layer_configuration in map_configuration.layer_configurations
        ]

        map_definition = MapDefinition(
            map_configuration.name,
            map_configuration.width,
            map_configuration.height,
            layers,
        )

        return map_definition

    def load(self) -> MapDefinition:
        map_configuration = self.map_configuration_loader.load_map_configuration()
        map_context = self.map_configuration_loader.load_map_context()

        map_definition = self.__generate_map_definition(map_configuration, map_context)

        return map_definition
