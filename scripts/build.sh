#!/bin/bash

black -l87 mapgen/ &&
flake8 mapgen/ --max-line-length=88 &&
mypy mapgen/ &&
pytest test/
