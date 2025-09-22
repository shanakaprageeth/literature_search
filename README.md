# PRISMA Search Literature Review Tool

## Overview
Automate and document literature reviews using the PRISMA methodology. Input a research topic or keywords, manage PRISMA data, and output publication lists and methodology text for research papers.

> **Disclaimer:**  
> Review and verify results before including them in research. Automated outputs assist, not replace, expert judgment.  
> **API Usage Notice:**  
> Use APIs responsibly to avoid rate limiting or loss of access.

## Features
- Flexible keyword input: list or comma-separated string
- Smart keyword handling: derives keywords from research topic if not provided
- Enhanced output: multiple CSVs for all and selected publications
- Collects PRISMA-related values (inclusion/exclusion criteria, databases, date ranges)
- Outputs:
  - PRISMA method data for literature review
  - CSVs: `all_publications_found.csv`, `selected_publications.csv`, `output_results.csv`
  - JSON file with results
  - PRISMA flow diagram in draw.io format (default or user template)
- Supports multiple databases: PubMed, CrossRef, arXiv, CORE, SemanticScholar
- Validates configuration files
- Retries API requests with exponential backoff
- Modular, extensible design

## PRISMA Flow Diagram Template

![PRISMA Flow Diagram](.assets/prisma_flow_diagram.drawio.svg)

Default template:  
`src/literature_search/prisma_flow_diagram.drawio`  
User template: place `prisma_flow_diagram.drawio` in output directory.  
Filled diagram: `prisma_flow_diagram_filled.drawio` in output directory.

## Configuration

### Keywords
Provide keywords as a list or comma-separated string:
```json
{
  "keywords": ["machine learning", "deep learning", "neural networks"]
}
```
or
```json
{
  "keywords": "machine learning, deep learning, neural networks"
}
```
If missing, keywords are generated from `research_topic` with a warning.

### Sample Configuration
```json
{
  "research_topic": "fundus image dataset",
  "keywords": "medical-imaging, machine-learning, fundus, retinal, ophthalmology",
  "initial_prisma_values": {
    "inclusion_criteria": ["review", "thesis", "journal", "book"],
    "exclusion_criteria": ["non-english", "conference"],
    "databases": ["PubMed", "CrossRef", "arXiv", "CORE", "SemanticScholar"],
    "date_range": "2015-2025"
  }
}
```

## Installation

Install via pip:
```bash
pip install literature_search
```
Or from wheel:
```bash
pip install dist/literature_search-*.whl
```

## Usage

### Console Script
Run from anywhere:
```bash
literature-search --config sample_input.json --logic OR --page_size 100 --output_dir output
```
Arguments:
- `--config`: Path to config JSON (default: sample_input.json)
- `--logic`: Keyword logic ('AND' or 'OR', default: OR)
- `--page_size`: Results per database (default: 100)
- `--output_dir`: Output directory (default: output)

### Programmatic Usage
Import and use in Python:
```python
from literature_search.config_loader import load_config
from literature_search.keywords import get_keywords
from literature_search.api_clients import (
    get_publications_europe_pmc,
    get_publications_crossref,
    get_publications_arxiv,
    get_publications_core,
    get_publications_semanticscholar
)
from literature_search.prisma_logs import output_prisma_results, create_prisma_drawio_diagram

config = load_config('sample_input.json')
keywords = get_keywords(config.get('research_topic', ''))
publications = get_publications_europe_pmc(keywords)
output_prisma_results(publications, criteria_counts, total_records, output_dir='output')
create_prisma_drawio_diagram(criteria_counts, total_records, output_dir='output')
```

## Output Files
- `all_publications_found.csv`: All publications with inclusion/exclusion info
- `selected_publications.csv`: Publications meeting inclusion criteria
- `output_results.csv`: All publications with inclusion status
- `results.json`: Complete results
- `prisma_flow_diagram.drawio`: PRISMA flow diagram

## Requirements
- Ubuntu 24.04.2 LTS
- Python 3.10+
- Python packages: `requests`, `drawpyo`, `matplotlib`, `pytest`

## Contributing

See `.github/copilot-instructions.md` for coding standards.

### Contribution Guide

1. Fork and create a feature branch.
2. Follow PEP 8 and PRISMA methodology.
3. Write clear commit messages and documentation.
4. Add tests for new features or fixes.
5. Submit a pull request.

### Package Publication

The package is automatically published to PyPI when:
1. Changes are merged to the main branch, AND
2. The commit message starts with `[release]`

For example: `[release] Version 1.0.0 with new features`

The publication uses PyPI OIDC (OpenID Connect) for secure authentication without requiring API tokens.

## License
GPL-3

## Future Work
- Add more database APIs
- AI-based abstract inclusion/exclusion