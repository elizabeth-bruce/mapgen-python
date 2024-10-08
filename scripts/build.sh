#!/bin/bash

black -l99 mapgen/ &&
flake8 mapgen/ --max-line-length=100 &&
mypy mapgen/ &&
pytest test/ &&
poetry run python test/run_lua_tests.py
