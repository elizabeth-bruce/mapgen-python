import os
import json

from mapgen.data.models import ViewConfiguration, ViewConfigurationSet, ViewSetContext
from mapgen.data.view_configuration_set_loader import ViewConfigurationSetLoader


class FileViewConfigurationSetLoader(ViewConfigurationSetLoader):
    def __init__(self, filename: str):
        self.filename = filename

    def load(self) -> ViewConfigurationSet:
        try:
            with open(self.filename, "r") as config_file:
                config_dict = json.load(config_file)
                view_configurations = [
                    ViewConfiguration(**view_configuration)
                    for view_configuration in config_dict["views"]
                ]

                view_configuration_set = ViewConfigurationSet(
                    view_configurations=view_configurations
                )

                return view_configuration_set
        except Exception as err:
            # TODO: Add logging support
            print(f"Error while loading file: {err}")
            raise err

    def load_view_set_context(self) -> ViewSetContext:
        map_file_path = os.path.dirname(self.filename)
        view_set_context = ViewSetContext(map_file_path)

        return view_set_context
