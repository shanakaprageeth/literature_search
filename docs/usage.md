# Usage Guide

This guide covers both command-line and programmatic usage of the Literature Review Tool.

## Command-Line Interface (CLI)

### Basic Usage

Run a literature search using a configuration file:

```bash
literature-search --config sample_input.json --logic OR --page_size 100 --output_dir output
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--config` | Path to JSON configuration file | `sample_input.json` |
| `--logic` | Keyword combination logic ('AND' or 'OR') | `OR` |
| `--page_size` | Number of results per database | `100` |
| `--output_dir` | Output directory for results | `output` |

### Examples

**Search with AND logic:**
```bash
literature-search --config my_config.json --logic AND --page_size 50
```

**Custom output directory:**
```bash
literature-search --config sample_input.json --output_dir my_results
```

**Minimal command (uses defaults):**
```bash
literature-search
```

## Programmatic Usage (Python API)

### Basic Example

```python
from literature_search.config_loader import load_config
from literature_search.keywords import get_keywords
from literature_search.api_clients import get_publications_europe_pmc
from literature_search.prisma_logs import output_prisma_results, create_prisma_drawio_diagram

# Load configuration
config = load_config('sample_input.json')

# Get keywords
keywords = get_keywords(config.get('research_topic', ''))

# Search a database
publications = get_publications_europe_pmc(keywords)

# Output results
output_prisma_results(publications, criteria_counts, total_records, output_dir='output')
create_prisma_drawio_diagram(criteria_counts, total_records, output_dir='output')
```

### Advanced Example: Multiple Databases

```python
from literature_search.config_loader import load_config
from literature_search.api_clients import (
    get_publications_europe_pmc,
    get_publications_crossref,
    get_publications_arxiv,
    get_publications_core,
    get_publications_semanticscholar,
    get_publications_ieee,
    get_publications_springer,
    get_publications_dblp,
    get_publications_scopus
)

# Load configuration
config = load_config('sample_input.json')
criteria = config['initial_prisma_values']
api_keys = config.get('api_keys', {})

# Search multiple databases
all_publications = []

# PubMed/Europe PMC (no API key required)
pmc_pubs = get_publications_europe_pmc(keywords)
all_publications.extend(pmc_pubs)

# CrossRef (no API key required)
crossref_pubs = get_publications_crossref(keywords)
all_publications.extend(crossref_pubs)

# arXiv (no API key required)
arxiv_pubs = get_publications_arxiv(keywords)
all_publications.extend(arxiv_pubs)

# CORE (API key required)
if 'CORE' in api_keys:
    core_pubs = get_publications_core(keywords, api_keys['CORE'])
    all_publications.extend(core_pubs)

# Process all publications
# ... apply filtering, generate outputs
```

### Using the Main Search Function

The recommended way to run a complete PRISMA search programmatically:

```python
from literature_search.cli import search_prisma

# Run the complete PRISMA workflow
search_prisma(
    config_file='my_config.json',
    logic='OR',
    page_size=100,
    output_dir='my_output'
)
```

## Output Files

After running a search, the following files are generated in the output directory:

### CSV Files

1. **`all_publications_found.csv`**
   - Contains all publications retrieved from databases
   - Includes inclusion/exclusion status
   - Shows reasons for exclusion
   - Best for comprehensive analysis

2. **`selected_publications.csv`**
   - Contains only publications meeting inclusion criteria
   - Filtered list ready for review
   - Best for starting your literature review

3. **`output_results.csv`**
   - All publications with inclusion status
   - Maintained for backward compatibility

### JSON Files

4. **`results.json`**
   - Complete results in JSON format
   - Includes all metadata
   - Useful for programmatic processing

### Diagram Files

5. **`prisma_flow_diagram.drawio`** (or `prisma_flow_diagram_filled.drawio`)
   - PRISMA flow diagram in draw.io format
   - Shows the systematic review process
   - Can be edited in draw.io or diagrams.net
   - Automatically filled with your search statistics

## Understanding Output

### CSV Column Descriptions

Common columns in output CSV files:

- **Title**: Publication title
- **Authors**: List of authors
- **Year**: Publication year
- **Journal**: Journal or venue name
- **DOI**: Digital Object Identifier (if available)
- **Abstract**: Publication abstract (if available)
- **Source**: Database source (PubMed, CrossRef, etc.)
- **Type**: Publication type (journal, conference, etc.)
- **Inclusion_Status**: Whether the publication was included/excluded
- **Exclusion_Reasons**: Reasons for exclusion (if applicable)

### PRISMA Statistics

The console output shows:
- Total records identified
- Records screened
- Records excluded (with breakdown by criteria)
- Records included in final analysis

## Error Handling

The tool includes robust error handling:

- **API failures**: Automatic retries with exponential backoff
- **Missing API keys**: Skips databases requiring keys with warnings
- **Invalid configuration**: Clear error messages with examples
- **Network issues**: Graceful degradation with informative messages

## Best Practices

1. **Start with a small page size** (e.g., 50) to test your configuration
2. **Review the console output** to understand what databases were searched
3. **Check exclusion reasons** in the CSV files to refine your criteria
4. **Use version control** for your configuration files
5. **Document your search parameters** in your research methodology
6. **Backup your output** directory before running new searches

## Next Steps

- [Configuration](configuration.md) - Learn about configuration options
- [Databases](databases.md) - Set up API keys for additional databases
- [FAQ](faq.md) - Common questions and troubleshooting
