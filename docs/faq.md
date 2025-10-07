# Frequently Asked Questions (FAQ)

## General Questions

### What is the Literature Review Tool?

The Literature Review Tool is a Python package that automates literature searches across multiple academic databases using the PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) methodology. It helps researchers systematically search, filter, and document literature reviews.

### Who should use this tool?

This tool is designed for:
- Researchers conducting systematic literature reviews
- Graduate students working on thesis literature reviews
- Academics preparing meta-analyses
- Anyone needing to search multiple databases systematically

### Is this tool free to use?

Yes, the tool itself is free and open-source (GPL-3.0 license). However, some databases require API keys:
- **Free**: PubMed, CrossRef, arXiv, CORE (free API key), SemanticScholar, DBLP
- **Paid/Institutional**: IEEE, Springer, Scopus

## Installation and Setup

### What are the system requirements?

- Ubuntu 24.04.2 LTS (or compatible Linux distribution)
- Python 3.9 or higher
- Dependencies: `requests`, `drawpyo`, `matplotlib`, `pytest`

### Can I use this on Windows or macOS?

The tool is developed for Linux (Ubuntu), but should work on:
- **macOS**: Generally compatible
- **Windows**: Should work with Python 3.9+, may need adjustments for file paths

### How do I install the tool?

Simply run:
```bash
pip install literature_search
```

See the [Installation Guide](installation.md) for details.

### I'm getting "permission denied" errors during installation. What should I do?

Try installing with user permissions:
```bash
pip install --user literature_search
```

Or use a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
pip install literature_search
```

## Configuration

### Do I need to provide keywords?

Keywords are optional. If you don't provide them, the tool will auto-generate keywords from your `research_topic` field with a warning message.

**Recommended**: Provide your own carefully chosen keywords for best results.

### What's the difference between inclusion and exclusion criteria?

- **Inclusion criteria**: Publications matching ANY of these will be INCLUDED
- **Exclusion criteria**: Publications matching ANY of these will be EXCLUDED (even if they match inclusion criteria)

Exclusion criteria take precedence over inclusion criteria.

### What is the field:value syntax?

The `field:value` syntax allows precise filtering:
```json
"inclusion_criteria": [
  "type:journal-article",
  "language:english",
  "journal:nature"
]
```

This is more precise than simple keywords. See [Configuration Guide](configuration.md#field-specific-criteria-advanced) for details.

### Can I use multiple databases at once?

Yes! Just list them in your configuration:
```json
"databases": ["PubMed", "CrossRef", "arXiv", "IEEE", "Springer"]
```

The tool will search all specified databases sequentially.

## API Keys

### Which databases require API keys?

- **Required**: CORE, IEEE, Springer, Scopus
- **Not required**: PubMed, CrossRef, arXiv, SemanticScholar, DBLP

### How do I get API keys?

See the [Databases Guide](databases.md) for detailed instructions for each database.

### What happens if I don't provide an API key for a required database?

The tool will skip that database with a warning message. Other databases will still be searched.

### Is it safe to put API keys in the configuration file?

**For development**: Yes, but never commit configuration files with API keys to version control.

**Best practices**:
- Add `*_config.json` to `.gitignore`
- Use environment variables for production
- Keep API keys secure and private

### My API key isn't working. What should I check?

1. Verify the key is correct (copy-paste errors are common)
2. Check the key hasn't expired
3. Ensure you're using the correct database name in the configuration
4. Verify your API key has proper permissions

## Usage

### How many results can I get per database?

Use the `--page_size` parameter to control this:
```bash
literature-search --config sample_input.json --page_size 100
```

**Recommendations**:
- Start with 50-100 for testing
- Use 100-500 for production searches
- Be mindful of API rate limits

### What does the `--logic` parameter do?

The `--logic` parameter controls how keywords are combined:
- **OR** (default): Returns publications matching ANY keyword
- **AND**: Returns publications matching ALL keywords

```bash
literature-search --config sample_input.json --logic AND
```

### Can I search a specific date range?

Yes, in your configuration file:
```json
"date_range": "2015-2025"
```

This filters publications to only those within the specified years.

### Why are my searches returning no results?

Common reasons:
1. **Keywords too specific**: Try broader terms
2. **Date range too narrow**: Expand the date range
3. **Criteria too restrictive**: Review inclusion/exclusion criteria
4. **Wrong database**: Some databases specialize in specific domains
5. **API key issues**: Check if databases are being skipped

## Output and Results

### What files are generated?

After a search, you'll find:
- `all_publications_found.csv` - All publications with status
- `selected_publications.csv` - Only included publications
- `output_results.csv` - Backward compatibility file
- `results.json` - Complete results in JSON
- `prisma_flow_diagram_filled.drawio` - PRISMA flow diagram

### What's the difference between the CSV files?

- **all_publications_found.csv**: Complete list with inclusion/exclusion reasons
- **selected_publications.csv**: Only publications that passed all criteria
- **output_results.csv**: Legacy format, kept for backward compatibility

Use `selected_publications.csv` for your literature review.

### How do I open the PRISMA flow diagram?

The `.drawio` file can be opened with:
- [draw.io](https://draw.io) (web-based, free)
- [diagrams.net](https://diagrams.net) (same as draw.io)
- Draw.io desktop application

### Can I customize the PRISMA diagram template?

Yes! Place your own `prisma_flow_diagram.drawio` file in the output directory before running the search. The tool will use your template and fill it with data.

### Why don't I see abstracts for all publications?

Not all databases provide abstracts:
- **Include abstracts**: PubMed, SemanticScholar, Springer
- **Limited abstracts**: CrossRef, IEEE, Scopus
- **No abstracts**: arXiv (uses summary instead), DBLP

## Troubleshooting

### "ERROR: Could not read configuration file"

- Check the file path is correct
- Verify JSON syntax (use a JSON validator)
- Ensure required fields are present
- Check file permissions

### "Rate limit exceeded" error

Some databases have rate limits:
1. Wait a few minutes before retrying
2. Reduce `--page_size` parameter
3. Spread searches over time
4. Check API documentation for limits

### The tool is hanging or running very slowly

Possible causes:
1. **Large page size**: Reduce `--page_size`
2. **Network issues**: Check internet connection
3. **API timeouts**: The tool retries automatically
4. **Multiple databases**: Searching many databases takes time

### I'm getting "Database not found" errors

Check the spelling of database names in your configuration:
- Correct: `"PubMed"`, `"CrossRef"`, `"arXiv"`
- Incorrect: `"pubmed"`, `"Crossref"`, `"arxiv"`

Database names are case-sensitive.

### How do I report bugs?

1. Check if it's already reported in [GitHub Issues](https://github.com/shanakaprageeth/literature_search/issues)
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Error messages
   - Your configuration (sanitized - remove API keys)
   - Environment details (OS, Python version)

## PRISMA Methodology

### What is PRISMA?

PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) is a framework for conducting systematic literature reviews. It ensures transparency and completeness in the review process.

Learn more: [PRISMA Statement](http://www.prisma-statement.org/)

### How does this tool implement PRISMA?

The tool implements PRISMA by:
1. **Identification**: Searching multiple databases systematically
2. **Screening**: Applying inclusion/exclusion criteria automatically
3. **Eligibility**: Filtering based on specified parameters
4. **Inclusion**: Generating final list of included publications
5. **Documentation**: Creating PRISMA flow diagrams and logs

### Do I still need to do manual review?

**Yes!** The tool automates searching and initial filtering, but you should:
1. Review abstracts of selected publications
2. Access full texts for final inclusion
3. Assess quality and relevance
4. Document any additional manual exclusions

See `prisma_guidelines.md` for manual review guidance.

### Can I use this for my thesis/dissertation?

Yes! However:
1. Document your search methodology clearly
2. Include search dates and database versions
3. Report the tool version used
4. Keep detailed records of your process
5. Follow your institution's requirements

### How should I cite this tool in my research?

```
Literature Review Tool (Version X.X.X). Shanaka Abeysiriwardhana. 
Available at: https://github.com/shanakaprageeth/literature_search
```

Also cite the specific database APIs you used.

## Advanced Usage

### Can I use this programmatically in my Python code?

Yes! See the [Usage Guide](usage.md#programmatic-usage-python-api) for examples.

### Can I add support for new databases?

Yes! See the [Contributing Guide](contributing.md#adding-a-new-database) for instructions.

### Can I integrate this with my existing workflow?

Yes! The tool provides:
- Command-line interface for scripts
- Python API for integration
- JSON output for downstream processing
- CSV output for spreadsheet analysis

### How can I process results further?

The `results.json` file contains complete data for further processing:
```python
import json

with open('output/results.json', 'r') as f:
    data = json.load(f)

# Process data as needed
for pub in data['publications']:
    # Your analysis here
    pass
```

## Performance

### How long does a typical search take?

Depends on:
- Number of databases: 1-3 minutes per database
- Page size: Larger sizes take longer
- Network speed: Affects API calls
- API response times: Varies by database

**Typical**: 5-15 minutes for 5 databases with page_size=100

### Can I speed up the search?

Optimization tips:
1. Reduce number of databases
2. Lower page_size for testing
3. Use more specific keywords
4. Narrow date range
5. Run during off-peak hours (better API response)

### Does the tool cache results?

No, the tool doesn't cache API results. Each search is fresh. If you need to re-process results without searching again, use the `results.json` file.

## Support and Community

### Where can I get help?

- **Documentation**: Read these docs thoroughly
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share experiences
- **Source Code**: Review code for implementation details

### How can I contribute?

See the [Contributing Guide](contributing.md) for detailed instructions.

### Is there a mailing list or forum?

Currently, we use GitHub for all community interaction:
- Issues for bugs and features
- Discussions for questions and ideas
- Pull requests for contributions

---

**Still have questions?** Open an issue on [GitHub](https://github.com/shanakaprageeth/literature_search/issues) or check the documentation.
