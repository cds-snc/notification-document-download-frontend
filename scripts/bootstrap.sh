#!/bin/sh
#
# Bootstrap virtualenv environment and postgres databases locally.
#
# NOTE: This script expects to be run from the project root with
# ./scripts/bootstrap.sh

# Install Python development dependencies
pip3 install -r requirements-dev.txt

npm install && npm run build
