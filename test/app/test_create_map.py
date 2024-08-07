import os
import re

from pathlib import Path
import pytest

from click.testing import CliRunner

from app.app import create

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

def test_create_map(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    result = runner.invoke(create)

    assert result.exit_code == 0

    assert os.path.exists(TEST_MAP_FILE_PATH)

    cleanup()

def test_create_map_with_config_file(runner, cleanup):
    result = runner.invoke(create, ['--config_file', MAP_CONFIGURATION_PATH])

    assert result.exit_code == 0
    assert os.path.exists(f"{os.getcwd()}/map.npz")

    cleanup(f"{os.getcwd()}/map.npz")

def test_create_map_with_out_file(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    result = runner.invoke(create, ['--out_file', 'test_name.npz'])

    assert result.exit_code == 0
    assert os.path.exists(f"{os.getcwd()}/test_name.npz")

    cleanup(f"{os.getcwd()}/test_name.npz")

def test_create_map_with_seed(runner, cleanup):
    os.chdir('/'.join(MAP_CONFIGURATION_PATH.split('/')[:-1]))

    result = runner.invoke(create, ['--seed', '9001'])

    assert result.exit_code == 0
    assert os.path.exists(TEST_MAP_FILE_PATH)

    cleanup()

def test_create_map_with_invalid_config_file(runner, cleanup):
    os.chdir('/'.join(INVALID_MAP_CONFIGURATION_PATH.split('/')[:-1]))

    result = runner.invoke(create)

    assert result.exit_code == 1

    ERROR_MESSAGE = "Error while loading file: 1 validation error for FrequencyFilteredNoiseContext"

    assert re.match(ERROR_MESSAGE, result.output)
    assert not os.path.exists(TEST_MAP_FILE_PATH)
