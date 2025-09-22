# PRISMA Search Literature Review Tool

## Overview
This project helps automate and document literature reviews using the PRISMA methodology. It allows users to input a research topic or keywords, manages PRISMA data, and outputs publication lists and methodology text for research papers.

> **Disclaimer:**  
> Use this tool at your own discretion. Always review and verify the results before including them in your research or publications. The automated outputs are intended to assist, not replace, expert judgment.  
> **API Usage Notice:**  
> Please do not overuse or misuse free APIs. Excessive requests may result in rate limiting or loss of access for yourself and others. Use the tool responsibly and respect the terms of service of each data provider.

## Features
- **Flexible keyword input**: Accept keywords as a list or comma-separated string in the configuration file
- **Smart keyword handling**: Automatically derives keywords from research topic if not provided, with warning message
- **Enhanced output**: Creates multiple CSV files showing all publications found and selected publications at each stage
- Collects initial PRISMA-related values (e.g., inclusion/exclusion criteria, databases, date ranges)
- Outputs:
  - PRISMA method data for literature review methods section
  - Multiple CSV files:
    - `all_publications_found.csv`: All publications with inclusion status and reasons
    - `selected_publications.csv`: Only included publications
    - `output_results.csv`: All publications with inclusion status (backward compatibility)
  - JSON file with complete results
  - PRISMA flow diagram in draw.io format (uses a default template if no user-provided template is found)
- Supports multiple databases: PubMed, CrossRef, arXiv, CORE, SemanticScholar
- Validates configuration files for correctness
- Retries API requests with exponential backoff for reliability
- Modular design for extensibility

## PRISMA Flow Diagram Template
The tool uses a default `prisma_flow_diagram.drawio` template located in the `src/literature_search_shanaka` package. If you want to use your own template, place it in the output directory with the name `prisma_flow_diagram.drawio`. The tool will prioritize the user-provided template over the default one.

Default template location:
```
src/literature_search_shanaka/prisma_flow_diagram.drawio
```

To use the default template, no additional configuration is required. The filled diagram will be saved as `prisma_flow_diagram_filled.drawio` in the output directory.

## Configuration

### Keywords Configuration
You can provide keywords in your configuration file in two ways:

1. **As a list** (original format):
```json
{
  "keywords": ["machine learning", "deep learning", "neural networks"]
}
```

2. **As a comma-separated string** (new format):
```json
{
  "keywords": "machine learning, deep learning, neural networks"
}
```

If no keywords are provided, the tool will automatically generate them from the `research_topic` and display a warning message.

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

You can install the package directly using pip:

```bash
pip install research-search-shanaka
```

Or if you have the wheel file:

```bash
pip install dist/literature_search_shanaka-*.whl
```

## Usage

### Console Script (Recommended)

Once installed, you can use the `prisma-search` command directly from anywhere:

```bash
prisma-search --config sample_input.json --logic OR --page_size 100 --output_dir output
```

The console script accepts the following arguments:
- `--config`: Path to config JSON file (default: sample_input.json)
- `--logic`: Keyword combination logic ('AND' or 'OR', default: OR)
- `--page_size`: Number of results per database (default: 100)
- `--output_dir`: Directory to save outputs (default: output)

### Alternative: Command Line Interface (Legacy)

You can also run the script directly if you have the repository:

```bash
python prisma_review.py --config sample_input.json --logic OR --page_size 100 --output_dir output
```

### Programmatic Usage
1. Import the package in your Python script:

```python
from literature_search_shanaka.config_loader import load_config
from literature_search_shanaka.keywords import get_keywords
from literature_search_shanaka.api_clients import (
    get_publications_europe_pmc,
    get_publications_crossref,
    get_publications_arxiv,
    get_publications_core,
    get_publications_semanticscholar
)
from literature_search_shanaka.prisma_logs import output_prisma_results, create_prisma_drawio_diagram
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

## Output Files
The tool creates the following output files in the specified output directory:
- `all_publications_found.csv`: All publications with inclusion status and exclusion reasons
- `selected_publications.csv`: Only the publications that meet inclusion criteria
- `output_results.csv`: All publications with inclusion status (for backward compatibility)
- `results.json`: Complete results in JSON format including criteria counts
- `prisma_flow_diagram.drawio`: PRISMA flow diagram for your research

## Requirements
- Ubuntu 24.04.2 LTS (dev container)
- Python 3.10+ (or as specified in implementation)
- Required Python packages (installed via `pip`):
  - `requests`
  - `drawpyo`
  - `matplotlib`
  - `pytest` (for testing)

## Contributing

See `.github/copilot-instructions.md` for coding standards.

### Contribution Guide for Developers

We welcome contributions from the community! To contribute:

1. **Fork the repository** and create your feature branch (`git checkout -b feature/my-feature`).
2. **Follow PEP 8** and PRISMA methodology for all code related to literature review features.
3. **Write clear commit messages** and document your changes.
4. **Add tests** for new features or bug fixes.
5. **Submit a pull request** describing your changes and referencing any related issues.

Please review `.github/copilot-instructions.md` for detailed coding standards and best practices.

## License
GPL-3

## Future Work
