# Configuration Guide

This guide explains how to configure the Literature Review Tool for your research needs.

## Configuration File Format

The tool uses JSON configuration files. Here's a complete example:

```json
{
  "research_topic": "fundus image dataset",
  "keywords": "medical-imaging, machine-learning, fundus, retinal, ophthalmology",
  "initial_prisma_values": {
    "inclusion_criteria": ["review", "thesis", "journal", "book"],
    "exclusion_criteria": ["non-english", "conference"],
    "databases": ["PubMed", "CrossRef", "arXiv", "CORE", "SemanticScholar", "IEEE", "Springer", "DBLP", "Scopus"],
    "date_range": "2015-2025"
  },
  "api_keys": {
    "CORE": "your_core_api_key_here",
    "IEEE": "your_ieee_api_key_here",
    "Springer": "your_springer_api_key_here",
    "Scopus": "your_scopus_api_key_here"
  }
}
```

## Configuration Fields

### Research Topic (Optional)

```json
"research_topic": "machine learning in healthcare"
```

- Free-text description of your research topic
- Used to auto-generate keywords if not provided
- Helps document your search scope

### Keywords

Keywords can be specified in two formats:

**List format:**
```json
"keywords": ["machine learning", "deep learning", "neural networks"]
```

**Comma-separated string:**
```json
"keywords": "machine learning, deep learning, neural networks"
```

**Auto-generated keywords:**
If you don't provide keywords, they'll be generated from the research topic with a warning:
```json
{
  "research_topic": "machine learning applications",
  "initial_prisma_values": { ... }
}
```

### PRISMA Values

The `initial_prisma_values` object contains PRISMA methodology parameters:

#### Inclusion Criteria

Publications matching ANY inclusion criterion will be included:

```json
"inclusion_criteria": ["review", "thesis", "journal", "book"]
```

#### Exclusion Criteria

Publications matching ANY exclusion criterion will be excluded:

```json
"exclusion_criteria": ["non-english", "conference", "preprint"]
```

#### Databases

List of databases to search:

```json
"databases": ["PubMed", "CrossRef", "arXiv", "CORE", "SemanticScholar", "IEEE", "Springer", "DBLP", "Scopus"]
```

Available databases:
- **PubMed** (Europe PMC): Medical and life sciences literature
- **CrossRef**: Scholarly publications across disciplines
- **arXiv**: Preprints in physics, math, CS, and more
- **CORE**: Open access research papers
- **SemanticScholar**: AI-powered academic search
- **IEEE**: Engineering and technology publications
- **Springer**: Academic publications
- **DBLP**: Computer science bibliography
- **Scopus**: Comprehensive academic database

#### Date Range

Filter publications by year:

```json
"date_range": "2015-2025"
```

Format: `"START_YEAR-END_YEAR"`

## Field-Specific Criteria (Advanced)

You can specify database-specific fields using the `field:value` format for more precise filtering:

```json
{
  "research_topic": "machine learning",
  "initial_prisma_values": {
    "inclusion_criteria": [
      "type:journal-article",
      "language:english",
      "journal:nature"
    ],
    "exclusion_criteria": [
      "type:conference-paper",
      "source:arxiv",
      "language:non-english"
    ],
    "databases": ["PubMed", "CrossRef", "arXiv"],
    "date_range": "2020-2025"
  }
}
```

### Supported Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `type` | Publication type | `journal-article`, `conference-paper`, `book-chapter` |
| `publication_type` | Alternate for type | Same as type |
| `pubtype` | Alternate for type | Same as type |
| `language` | Publication language | `english`, `spanish`, `french` |
| `source` | Database source | `pubmed`, `arxiv`, `crossref` |
| `journal` | Journal name | `nature`, `science`, `plos one` |
| `venue` | Venue name (conferences) | Same as journal |
| `authors` | Author names | Author name to search |
| `document_type` | Document type (CORE) | Document classification |

### Database-Specific Mappings

Different databases use different field names. The tool automatically maps your criteria to the appropriate field:

#### PubMed/Europe PMC
- `type` → Publication type from medical literature
- `language` → Publication language
- `journal` → Journal name

#### CrossRef
- `type` → Publication type metadata
- `language` → Publication language
- `journal` → Container title

#### arXiv
- `type` → Publication type (preprint)
- Categories as metadata

#### CORE
- `document_type` → Mapped to Type field
- `type` → Document type

#### SemanticScholar
- `venue` → Mapped to Journal field
- `journal` → Publication venue

#### IEEE, Springer, DBLP, Scopus
- Similar mappings with database-specific adaptations

### Backward Compatibility

Criteria without field specifications default to the `type` field:

```json
"inclusion_criteria": ["journal", "review"]
```

This is equivalent to:
```json
"inclusion_criteria": ["type:journal", "type:review"]
```

## API Keys

Some databases require API keys. Add them to the `api_keys` section:

```json
"api_keys": {
  "CORE": "your_core_api_key",
  "IEEE": "your_ieee_api_key",
  "Springer": "your_springer_api_key",
  "Scopus": "your_scopus_api_key"
}
```

See [Databases](databases.md) for information on obtaining API keys.

## Example Configurations

### Minimal Configuration

```json
{
  "research_topic": "artificial intelligence",
  "initial_prisma_values": {
    "inclusion_criteria": ["journal"],
    "exclusion_criteria": ["conference"],
    "databases": ["PubMed", "CrossRef"],
    "date_range": "2020-2024"
  }
}
```

### Comprehensive Configuration

```json
{
  "research_topic": "deep learning for medical imaging",
  "keywords": ["deep learning", "medical imaging", "neural networks", "radiology", "diagnosis"],
  "initial_prisma_values": {
    "inclusion_criteria": [
      "type:journal-article",
      "type:review",
      "language:english"
    ],
    "exclusion_criteria": [
      "type:conference-paper",
      "type:preprint",
      "language:non-english"
    ],
    "databases": ["PubMed", "CrossRef", "IEEE", "Springer", "Scopus"],
    "date_range": "2018-2024"
  },
  "api_keys": {
    "IEEE": "your_ieee_api_key",
    "Springer": "your_springer_api_key",
    "Scopus": "your_scopus_api_key"
  }
}
```

### Computer Science Research

```json
{
  "research_topic": "blockchain security",
  "keywords": ["blockchain", "security", "cryptography", "distributed systems"],
  "initial_prisma_values": {
    "inclusion_criteria": [
      "type:journal-article",
      "language:english"
    ],
    "exclusion_criteria": [
      "type:conference-paper"
    ],
    "databases": ["arXiv", "DBLP", "IEEE", "SemanticScholar"],
    "date_range": "2019-2024"
  },
  "api_keys": {
    "IEEE": "your_ieee_api_key"
  }
}
```

## Configuration Validation

The tool validates your configuration file and provides helpful error messages:

- **Missing required fields**: Clear error with expected format
- **Invalid field types**: Examples of correct format
- **Missing API keys**: Warnings when databases requiring keys are skipped
- **Malformed JSON**: Syntax error location

## Best Practices

1. **Start simple**: Use a basic configuration and refine iteratively
2. **Test with small page sizes**: Verify your configuration works before large searches
3. **Version control**: Keep your configurations in version control
4. **Document your choices**: Add comments in a separate README
5. **Review exclusions**: Check exclusion reasons to refine criteria
6. **Use meaningful names**: Save configs with descriptive filenames (e.g., `ml_healthcare_2024.json`)

## Next Steps

- [Usage](usage.md) - Learn how to run searches with your configuration
- [Databases](databases.md) - Get API keys for additional databases
- [FAQ](faq.md) - Troubleshooting configuration issues
