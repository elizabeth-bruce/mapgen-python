import click

import os

from mapgen.data.models import ViewConfiguration

from mapgen.data.layer_configuration_loader import LayerConfigurationLoader
from mapgen.data.file_map_configuration_loader import FileMapConfigurationLoader

from mapgen.data.map_definition_loader import MapDefinitionLoader

from mapgen.data.file_view_configuration_set_loader import FileViewConfigurationSetLoader
from mapgen.data.console_map_viewer import ConsoleMapViewer

from mapgen.use_cases.map_creator import MapCreator

from mapgen.data.compressed_npz_map_saver import CompressedNpzMapSaver
from mapgen.data.compressed_npz_map_loader import CompressedNpzMapLoader

def render_view_configuration(view_configuration: ViewConfiguration) -> str:
    return f"- {view_configuration.name} (type: {view_configuration.type})"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config_file', default='configuration.json', help='Configuration file to use when creating map.')
@click.option('--out_file', default='map.npz', help='Location to write the created map to.')
@click.option('--seed', default=1, help='Seed for the random generator used when creating map.')
def create(config_file: str, out_file: str, seed: int) -> None:
    ROOT_DIR = os.path.abspath(os.curdir)

    layer_configuration_loader = LayerConfigurationLoader()
    map_configuration_loader = FileMapConfigurationLoader(os.path.join(ROOT_DIR, config_file))

    map_definition_loader = MapDefinitionLoader(layer_configuration_loader, map_configuration_loader)

    map_configuration = map_configuration_loader.load_map_configuration()
    map_context = map_configuration_loader.load_map_context()
    map_definition = map_definition_loader.load()

    map_creator = MapCreator()
    new_map = map_creator.create_map(map_definition, seed)

    map_saver = CompressedNpzMapSaver()
    map_saver.save(new_map, out_file)

@cli.command('list-views')
@click.option('--view_file', default='views.json', help='View configuration file to load map views from.')
def list_views(view_file: str) -> None:
    ROOT_DIR = os.path.abspath(os.curdir)

    view_configuration_set_loader = FileViewConfigurationSetLoader(os.path.join(ROOT_DIR, view_file))
    view_configuration_set = view_configuration_set_loader.load()

    for view_configuration in view_configuration_set.view_configurations:
        click.echo(render_view_configuration(view_configuration))

@cli.command()
@click.option('--map_file', default='map.npz', help='Location to read the map from.')
@click.option('--view_file', default='views.json', help='View configuration file to load map views from.')
@click.argument('view')
def view(map_file: str, view_file: str, view: str) -> None:
    ROOT_DIR = os.path.abspath(os.curdir)

    map_loader = CompressedNpzMapLoader()
    new_map = map_loader.load(os.path.join(ROOT_DIR, map_file))

    view_configuration_set_loader = FileViewConfigurationSetLoader(os.path.join(ROOT_DIR, view_file))

    view_configuration_set = view_configuration_set_loader.load()
    view_set_context = view_configuration_set_loader.load_view_set_context()

    console_map_viewer = ConsoleMapViewer(view_configuration_set, view_set_context)
    render_str = console_map_viewer.render(new_map, view)

    click.echo(render_str)
