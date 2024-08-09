import os
import re

from pathlib import Path
import pytest

from click.testing import CliRunner

from app.app import create, view

ROOT_DIR = os.path.abspath(os.curdir)
MAP_CONFIGURATION_PATH = f"{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/configuration.json"
TEST_MAP_FILE_PATH = f"{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/map.npz"

INVALID_MAP_CONFIGURATION_PATH = f"{ROOT_DIR}/test/resources/data/maps/invalid_configuration_map/configuration.json"

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def cleanup(request):
    def _cleanup(file_path=TEST_MAP_FILE_PATH):
        def remove_test_map_file():
            Path.unlink(file_path)
        request.addfinalizer(remove_test_map_file)

    return _cleanup

def test_view_map(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    runner.invoke(create)

    result = runner.invoke(view, ['temperature'])

    expected_output = """@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
"""

    assert result.output == expected_output
    cleanup()

def test_view_map_with_map_file(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    runner.invoke(create)

    result = runner.invoke(view, ['--map_file', 'map.npz', 'temperature'])
    expected_output = """@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
@@@@@@@@@@
"""

    assert result.output == expected_output
    cleanup()

def test_view_map_with_invalid_map_file(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    runner.invoke(create)

    result = runner.invoke(view, ['--map_file', 'not_a_map.npz', 'temperature'])

    error_message = "Error while loading file: \[Errno 2\] No such file or directory"

    assert result.exit_code == 1
    cleanup()

def test_view_map_with_invalid_view(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    runner.invoke(create)

    result = runner.invoke(view, ['fake_view'])

    assert result.exit_code == 1
    cleanup()
