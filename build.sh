#!/bin/bash
set -e

# Uninstall old version if exists
echo "Uninstalling old research_search_shanaka if present..."
pip3 uninstall -y research_search_shanaka || true

# Build the package
python3 -m pip install --upgrade build
python3 -m build

# Install the new package
echo "Installing new research_search_shanaka..."
pip3 install dist/research_search_shanaka-*.whl