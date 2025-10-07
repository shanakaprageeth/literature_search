# Supported Databases

The Literature Review Tool supports 9 academic databases for comprehensive literature searches.

## Database Overview

| Database | API Key Required | Domain | Description |
|----------|------------------|--------|-------------|
| PubMed (Europe PMC) | No | Medical/Life Sciences | Medical and life sciences literature |
| CrossRef | No | Multidisciplinary | Scholarly publications metadata |
| arXiv | No | STEM | Preprints in physics, math, CS, etc. |
| CORE | Yes | Multidisciplinary | Open access research papers |
| SemanticScholar | No | Multidisciplinary | AI-powered academic search |
| IEEE Xplore | Yes | Engineering/Tech | Engineering and technology publications |
| Springer Nature | Yes | Multidisciplinary | Academic publications across disciplines |
| DBLP | No | Computer Science | Computer science bibliography |
| Scopus | Yes | Multidisciplinary | Comprehensive academic database |

## Databases Not Requiring API Keys

### PubMed (Europe PMC)

**Domain**: Medical and life sciences literature

**Access**: Free, no API key required

**Features**:
- Comprehensive medical literature coverage
- PubMed and PubMed Central content
- Metadata including abstracts, authors, journals
- Date range filtering

**Usage in config**:
```json
"databases": ["PubMed"]
```

### CrossRef

**Domain**: Multidisciplinary scholarly publications

**Access**: Free, no API key required

**Features**:
- Extensive scholarly publication metadata
- DOI-based identification
- Journal articles, books, conference proceedings
- Date range filtering

**Usage in config**:
```json
"databases": ["CrossRef"]
```

### arXiv

**Domain**: Preprints in physics, mathematics, computer science, and more

**Access**: Free, no API key required

**Features**:
- Open access preprints
- Recent research before peer review
- Strong coverage in physics, math, CS
- Category-based classification

**Usage in config**:
```json
"databases": ["arXiv"]
```

### SemanticScholar

**Domain**: AI-powered multidisciplinary academic search

**Access**: Free, no API key required

**Features**:
- AI-powered relevance ranking
- Citation data
- Influential papers identification
- Multidisciplinary coverage

**Usage in config**:
```json
"databases": ["SemanticScholar"]
```

### DBLP

**Domain**: Computer science bibliography

**Access**: Free, no API key required

**Features**:
- Comprehensive CS publication database
- Conference and journal coverage
- Author disambiguation
- Venue tracking

**Usage in config**:
```json
"databases": ["DBLP"]
```

## Databases Requiring API Keys

### CORE

**Domain**: Open access research papers

**Access**: Requires free API key

**How to get API key**:
1. Visit [CORE API Portal](https://core.ac.uk/services/api)
2. Register for a free account
3. Request API key from your dashboard
4. Add to configuration file

**Features**:
- Open access focus
- Full-text access to many papers
- Metadata extraction
- Repository aggregation

**Usage in config**:
```json
{
  "databases": ["CORE"],
  "api_keys": {
    "CORE": "your_core_api_key_here"
  }
}
```

### IEEE Xplore

**Domain**: Engineering and technology publications

**Access**: Requires API key

**How to get API key**:
1. Visit [IEEE Developer Portal](https://developer.ieee.org/docs)
2. Create an IEEE account
3. Apply for API access
4. Receive API key via email

**Features**:
- IEEE publications
- IET content
- Conference proceedings
- Standards and specifications

**Usage in config**:
```json
{
  "databases": ["IEEE"],
  "api_keys": {
    "IEEE": "your_ieee_api_key_here"
  }
}
```

### Springer Nature

**Domain**: Multidisciplinary academic publications

**Access**: Requires API key

**How to get API key**:
1. Visit [Springer Nature API Portal](https://dev.springernature.com/)
2. Register for an account
3. Create an application
4. Get your API key

**Features**:
- Springer and Nature journals
- Book chapters
- Conference proceedings
- High-quality peer-reviewed content

**Usage in config**:
```json
{
  "databases": ["Springer"],
  "api_keys": {
    "Springer": "your_springer_api_key_here"
  }
}
```

### Scopus

**Domain**: Comprehensive multidisciplinary academic database

**Access**: Requires API key (institutional access typically required)

**How to get API key**:
1. Visit [Elsevier Developer Portal](https://dev.elsevier.com/)
2. Register with institutional credentials
3. Create an application
4. Receive API key

**Features**:
- Largest abstract and citation database
- Author profiles
- Institution tracking
- Citation analysis
- Comprehensive coverage across disciplines

**Usage in config**:
```json
{
  "databases": ["Scopus"],
  "api_keys": {
    "Scopus": "your_scopus_api_key_here"
  }
}
```

## Choosing Databases

### By Research Domain

**Medical/Life Sciences**:
- PubMed (essential)
- CrossRef
- Scopus (if available)

**Computer Science**:
- DBLP (essential)
- arXiv
- IEEE
- SemanticScholar

**Engineering**:
- IEEE (essential)
- Scopus (if available)
- Springer

**Multidisciplinary**:
- CrossRef
- SemanticScholar
- CORE
- Scopus (if available)

**Open Access Focus**:
- CORE
- arXiv
- PubMed Central

### By Budget/Access

**Free (no API keys needed)**:
- PubMed
- CrossRef
- arXiv
- SemanticScholar
- DBLP

**Free API keys**:
- CORE

**Paid/Institutional access**:
- IEEE
- Springer
- Scopus

## API Rate Limits and Best Practices

### General Guidelines

1. **Respect rate limits**: The tool includes automatic retries, but be considerate
2. **Start small**: Test with `page_size=50` before large searches
3. **Sequential searches**: Don't run multiple searches simultaneously
4. **API key security**: Never commit API keys to version control
5. **Fair use**: Follow each provider's terms of service

### Database-Specific Limits

- **PubMed**: Generally generous limits
- **CrossRef**: Polite mode implemented (recommended)
- **arXiv**: Rate limiting on heavy use
- **CORE**: Fair use policy
- **SemanticScholar**: Rate limits apply
- **IEEE**: Depends on API tier
- **Springer**: Depends on agreement
- **DBLP**: Generally open
- **Scopus**: Institutional limits

## Troubleshooting

### Database Not Returning Results

1. Check API key is correct
2. Verify keywords are appropriate for the database
3. Check date range is reasonable
4. Review console output for error messages

### API Key Issues

**"API key required" warning**:
- Add the API key to your configuration file
- Verify the key is valid
- Check you're using the correct key for the database

**"Invalid API key" error**:
- Verify the key is correct
- Check the key hasn't expired
- Ensure you're using the key for the right database

### Rate Limiting

**"Rate limit exceeded" error**:
- Wait before retrying
- Reduce `page_size` parameter
- Consider spreading searches over time

## Example Multi-Database Configuration

```json
{
  "research_topic": "machine learning applications in healthcare",
  "keywords": ["machine learning", "healthcare", "diagnosis", "prediction"],
  "initial_prisma_values": {
    "inclusion_criteria": ["type:journal-article", "language:english"],
    "exclusion_criteria": ["type:conference-paper"],
    "databases": [
      "PubMed",
      "CrossRef",
      "IEEE",
      "Springer",
      "SemanticScholar",
      "Scopus"
    ],
    "date_range": "2019-2024"
  },
  "api_keys": {
    "IEEE": "your_ieee_key",
    "Springer": "your_springer_key",
    "Scopus": "your_scopus_key"
  }
}
```

## Next Steps

- [Configuration](configuration.md) - Configure your database searches
- [Usage](usage.md) - Run searches across databases
- [FAQ](faq.md) - Common database-related questions
