# Installation

## Requirements

- **Operating System**: Ubuntu 24.04.2 LTS (or compatible Linux distribution)
- **Python**: 3.9 or higher
- **Python Packages**: `requests`, `drawpyo`, `matplotlib`, `pytest`

## Installation Methods

### Install from PyPI (Recommended)

The easiest way to install the Literature Review Tool is via pip from PyPI:

```bash
pip install literature_search
```

This will install the latest stable version with all required dependencies.

### Install from Wheel File

If you have a pre-built wheel file:

```bash
pip install dist/literature_search-*.whl
```

### Install from Source

To install from the source repository:

1. Clone the repository:
   ```bash
   git clone https://github.com/shanakaprageeth/literature_search.git
   cd literature_search
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build and install:
   ```bash
   python -m build
   pip install dist/literature_search-*.whl
   ```

## Verifying Installation

After installation, verify that the tool is correctly installed by running:

```bash
literature-search --help
```

You should see the help message with available options.

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade literature_search
```

## Uninstalling

To remove the Literature Review Tool:

```bash
pip uninstall literature-search
```

## Dependencies

The tool automatically installs the following dependencies:

- **matplotlib** (≥3.10.3): For plotting and visualization
- **drawpyo** (≥0.2.2): For generating PRISMA flow diagrams
- **requests**: For API calls to databases
- **pytest**: For running tests (development)

## Troubleshooting

### Permission Errors

If you encounter permission errors during installation:

```bash
pip install --user literature_search
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install literature_search
```

### Python Version Issues

Ensure you're using Python 3.9 or higher:

```bash
python --version
```

If you have multiple Python versions, you may need to specify:

```bash
python3.9 -m pip install literature_search
```

### Missing Dependencies

If dependencies fail to install automatically, install them manually:

```bash
pip install matplotlib>=3.10.3 drawpyo>=0.2.2 requests pytest
```

## Next Steps

After installation, proceed to:
- [Configuration](configuration.md) - Set up your configuration file
- [Usage](usage.md) - Learn how to use the tool
- [Databases](databases.md) - Configure API keys for databases
