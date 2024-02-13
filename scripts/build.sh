#!/bin/bash

black -l80 mapgen/ &&
flake8 mapgen/ &&
mypy mapgen/ &&
pytest test/
