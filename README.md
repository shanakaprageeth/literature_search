# PRISMA Search Literature Review Tool

## Overview
This project helps automate and document literature reviews using the PRISMA methodology. It allows users to input a research topic or keywords, manages PRISMA data, and outputs publication lists and methodology text for research papers.

## Features
- Accepts research topic or keywords from the user
- Automatically derives keywords if only a topic is provided
- Collects initial PRISMA-related values (e.g., inclusion/exclusion criteria, databases, date ranges)
- Outputs:
  - PRISMA method data for literature review methods section
  - CSV file of selected publications
  - PRISMA flow diagram in draw.io format
- Supports multiple databases: PubMed, CrossRef, arXiv, CORE, SemanticScholar
- Validates configuration files for correctness
- Retries API requests with exponential backoff for reliability
- Modular design for extensibility

## Installation
To install the `research_search_shanaka` pip package, run:

```bash
pip install dist/research_search_shanaka-*.whl
```

## Usage
1. Import the package in your Python script:

```python
from research_search_shanaka.config_loader import load_config
from research_search_shanaka.keywords import get_keywords
from research_search_shanaka.api_clients import (
    get_publications_europe_pmc,
    get_publications_crossref,
    get_publications_arxiv,
    get_publications_core,
    get_publications_semanticscholar
)
from research_search_shanaka.prisma_logs import output_prisma_results, create_prisma_drawio_diagram
```

2. Use the provided functions to load configurations, fetch publications, and generate PRISMA outputs.

3. Example:

```python
config = load_config('sample_input.json')
keywords = get_keywords(config.get('research_topic', ''))
publications = get_publications_europe_pmc(keywords)
output_prisma_results(publications, criteria_counts, total_records, output_dir='output')
create_prisma_drawio_diagram(criteria_counts, total_records, output_dir='output')
```

## Output
- `prisma_method.txt`: Text for your literature review methods section
- `selected_publications.csv`: List of selected publications
- `prisma_flow_diagram.drawio`: PRISMA flow diagram for your research

## Requirements
- Ubuntu 24.04.2 LTS (dev container)
- Python 3.10+ (or as specified in implementation)
- Required Python packages (installed via `pip`):
  - `requests`
  - `drawpyo`
  - `matplotlib`

## Contributing
See `.github/copilot-instructions.md` for coding standards.

## License
GPL-3

"databases": ["PubMed", "CrossRef", "arXiv", "CORE", "SemanticScholar"],