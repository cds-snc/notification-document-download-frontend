#!/bin/sh
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

flake8 .

isort --check-only -rc ./app ./tests

npm test

py.test tests/
