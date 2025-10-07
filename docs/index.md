# Literature Review Tool

[![PyPI version](https://img.shields.io/pypi/v/literature-search.svg)](https://pypi.org/project/literature-search/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Welcome

Welcome to the Literature Review Tool documentation! This tool automates and documents literature reviews using the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology.

> **Disclaimer:**  
> Review and verify results before including them in research. Automated outputs assist, not replace, expert judgment.  
> **API Usage Notice:**  
> Use APIs responsibly to avoid rate limiting or loss of access.

## Overview

The Literature Review Tool helps researchers:
- Automate literature searches across multiple academic databases
- Apply PRISMA methodology for systematic reviews
- Filter publications using inclusion/exclusion criteria
- Generate PRISMA flow diagrams automatically
- Export results in multiple formats (CSV, JSON)
- Document methodology for research papers

## Key Features

- **Flexible keyword input**: List or comma-separated string format
- **Smart keyword handling**: Auto-derives keywords from research topic
- **Database-specific field mapping**: Advanced filtering with `field:value` syntax
- **Multiple output formats**: CSV files for all and selected publications
- **PRISMA flow diagrams**: Auto-generated draw.io format diagrams
- **Multi-database support**: PubMed, CrossRef, arXiv, CORE, SemanticScholar, IEEE Xplore, Springer, DBLP, Scopus
- **Robust API handling**: Retries with exponential backoff
- **Modular design**: Easy to extend and customize

## Quick Start

Install via pip:
```bash
pip install literature_search
```

Run a literature search:
```bash
literature-search --config sample_input.json --logic OR --page_size 100 --output_dir output
```

## PRISMA Flow Diagram

The tool automatically generates PRISMA flow diagrams following the standard methodology:

![PRISMA Flow Diagram](https://raw.githubusercontent.com/shanakaprageeth/literature_search/main/.assets/prisma_flow_diagram.drawio.svg)

## Documentation Sections

- **[Installation](installation.md)**: Installation instructions and requirements
- **[Usage](usage.md)**: How to use the tool (CLI and programmatic)
- **[Configuration](configuration.md)**: Configuration file format and options
- **[Databases](databases.md)**: Supported databases and API keys
- **[Contributing](contributing.md)**: How to contribute to the project
- **[FAQ](faq.md)**: Frequently asked questions

## Getting Help

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/shanakaprageeth/literature_search/issues)
- **Discussions**: Join conversations on GitHub Discussions
- **Source Code**: View the source on [GitHub](https://github.com/shanakaprageeth/literature_search)

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](https://github.com/shanakaprageeth/literature_search/blob/main/LICENSE) file for details.

---

**Copyright © 2024 Shanaka Abeysiriwardhana**
