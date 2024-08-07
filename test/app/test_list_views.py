import os
import re

from pathlib import Path
import pytest

from click.testing import CliRunner

from app.app import list_views

ROOT_DIR = os.path.abspath(os.curdir)
VIEW_PATH = f"{ROOT_DIR}/test/resources/data/maps/filtered_noise_map/views.json"

@pytest.fixture
def runner():
    return CliRunner()

def test_list_views(runner):
    os.chdir('/'.join(VIEW_PATH.split('/')[:-1]))

    result = runner.invoke(list_views)

    expected_output = """- temperature (type: CONSOLE)\n"""

    assert result.exit_code == 0
    assert result.output == expected_output

def test_list_views_with_view_file(runner):
    result = runner.invoke(list_views, ['--view_file', VIEW_PATH])

    expected_output = """- temperature (type: CONSOLE)\n"""

    assert result.exit_code == 0
    assert result.output == expected_output

def test_list_views_with_invalid_view_file(runner):
    result = runner.invoke(list_views, ['--view_file', "bad_path.json"])

    error_message = "Error while loading file: \[Errno 2\] No such file or directory"

    assert result.exit_code == 1
    assert re.match(error_message, result.output)
