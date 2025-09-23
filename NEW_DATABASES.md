# New Database Support Demo

This repository now supports 4 additional databases for comprehensive literature search:

## New Databases Added

1. **IEEE Xplore** - Engineering and technology publications
2. **Springer Nature** - Academic publications across disciplines  
3. **DBLP** - Computer science publications database
4. **Scopus** - Comprehensive academic database

## Quick Start

Update your configuration file to include the new databases:

```json
{
  "research_topic": "your research topic",
  "keywords": ["keyword1", "keyword2"],
  "initial_prisma_values": {
    "inclusion_criteria": ["type:journal", "language:english"],
    "exclusion_criteria": ["type:conference"],
    "databases": ["PubMed", "IEEE", "Springer", "DBLP", "Scopus"],
    "date_range": "2020-2025"
  },
  "api_keys": {
    "IEEE": "your_ieee_api_key",
    "Springer": "your_springer_api_key", 
    "Scopus": "your_scopus_api_key"
  }
}
```

## API Key Requirements

- **IEEE**: Required - Get from [IEEE Developer Portal](https://developer.ieee.org/docs)
- **Springer**: Required - Get from [Springer Nature API](https://dev.springernature.com/)
- **DBLP**: No API key required
- **Scopus**: Required - Get from [Elsevier Developer Portal](https://dev.elsevier.com/)

## Features

- All databases support keyword search with AND/OR logic
- Date range filtering where supported by the API
- Metadata extraction (titles, authors, journals, DOIs, abstracts)
- Integration with existing criteria mapping system
- Comprehensive error handling and retry logic

Run the demo script to see the new functionality in action:

```bash
python /tmp/demo_new_databases.py
```