#!/bin/bash

black -l79 mapgen/ &&
flake8 mapgen/ &&
mypy mapgen/ &&
pytest test/
