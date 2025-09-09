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
- Notifies user if manual abstract review is needed, with guidelines and sample methodology text

## Usage
1. Start the tool and provide your research topic or keywords.
2. Enter initial PRISMA values as prompted (criteria, databases, etc.).
3. Review the generated PRISMA data and publication list.
4. If manual review is required, follow the provided guidelines and include the suggested methodology in your paper.

## Output
- `prisma_method.txt`: Text for your literature review methods section
- `selected_publications.csv`: List of selected publications

## Requirements
- Ubuntu 24.04.2 LTS (dev container)
- Python 3.10+ (or as specified in implementation)

## Contributing
See `copilot-instructions.md` for coding standards.

## License
MIT

"databases": ["PubMed", "CrossRef", "arXiv", "CORE", "SemanticScholar"],