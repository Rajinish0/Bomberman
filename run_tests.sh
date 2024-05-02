#!/usr/bin/env bash

# script for running tests on unix based os

export PYTHONPATH='./'
python3 -m unittest discover -s tests -p "test_*.py"
