#!/bin/bash
set -e

usage() {
    echo "Usage: $0 [build|test|publish]"
    echo "  build   : Build the package (default)"
    echo "  test    : Build and test the package"
    echo "  publish : Build, test, and publish the package"
    exit 1
}

# Default action
ACTION=${1:-build}

# Build the package
if [[ "$ACTION" == "build" || "$ACTION" == "test" || "$ACTION" == "publish" ]]; then
    echo "Building the package..."
    python3 -m pip install --upgrade build
    python3 -m pip install -r requirements.txt
    python3 -m build
fi

# Test the package
if [[ "$ACTION" == "test" || "$ACTION" == "publish" ]]; then
    echo "Installing new literature_search..."
    pip3 install dist/literature_search-*.whl

    echo "Running tests..."
    pytest tests
    literature-search --config sample_input.json
fi

# Publish the package
if [[ "$ACTION" == "publish" ]]; then
    echo "Verifying the package..."
    python3 -m twine check dist/*

    echo "Uploading the package to PyPI..."
    python3 -m twine upload dist/*
fi

echo "Done."