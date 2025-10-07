# Contributing to Literature Review Tool

Thank you for your interest in contributing to the Literature Review Tool! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git for version control
- Understanding of PRISMA methodology
- Familiarity with Python best practices (PEP 8)

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/literature_search.git
   cd literature_search
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install development tools**:
   ```bash
   pip install pytest
   ```

## Coding Standards

### Style Guide

We follow PEP 8 coding style and conventions. Key points:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 120 characters (preferred 80-100)
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Docstrings**: Use Google-style or NumPy-style docstrings
- **Type hints**: Use type hints for function arguments and return values

### Example Function

```python
def search_database(
    keyword_list: List[str],
    api_key: Optional[str] = None,
    page_size: int = 100,
    db_name: str = 'PubMed'
) -> List[Dict[str, Any]]:
    """Search a database for publications matching keywords.
    
    Args:
        keyword_list: List of keywords to search for
        api_key: Optional API key for the database
        page_size: Number of results to retrieve (default: 100)
        db_name: Name of the database to search
        
    Returns:
        List of publication dictionaries with metadata
        
    Raises:
        ValueError: If database name is invalid
        APIError: If API request fails
    """
    # Implementation here
    pass
```

### PRISMA Methodology

- Follow PRISMA guidelines for all literature review features
- Maintain clear documentation of the systematic review process
- Ensure proper filtering and reporting mechanisms

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-new-database` - New features
- `bugfix/fix-api-error` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/improve-performance` - Code refactoring

### 2. Make Changes

- Write clear, focused commits
- Follow coding standards
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

Run the test suite:
```bash
pytest tests/
```

Run specific tests:
```bash
pytest tests/test_config_loader.py
```

Run with coverage:
```bash
pytest --cov=literature_search tests/
```

### 4. Commit Changes

Write clear commit messages:
```bash
git commit -m "Add support for new database X"
```

Good commit message format:
```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain what changes were made and why.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")
- Reference issues: "Fixes #123"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference to related issues
- Summary of changes
- Testing done
- Screenshots (if applicable)

## Types of Contributions

### Bug Reports

When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages or logs
- Configuration file (sanitized, no API keys)

### Feature Requests

When suggesting features:
- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider backward compatibility
- Provide use cases

### Code Contributions

Focus areas:
- **New database support**: Add connectors for additional databases
- **Performance improvements**: Optimize API calls and data processing
- **Error handling**: Improve error messages and recovery
- **Testing**: Add or improve test coverage
- **Documentation**: Improve guides and API documentation

### Documentation Contributions

Help improve:
- User guides and tutorials
- API documentation
- Code comments
- README and examples
- FAQ entries

## Adding a New Database

To add support for a new database:

1. **Create API client function** in `src/literature_search/api_clients.py`:
   ```python
   def get_publications_newdb(keyword_list, api_key=None, page_size=100, logic='OR'):
       """Fetch publications from NewDB."""
       # Implementation
       pass
   ```

2. **Add database mapping** in `src/literature_search/criteria_mapper.py`:
   ```python
   'NewDB': {
       'type': 'Type',
       'language': 'Language',
       'journal': 'Journal'
   }
   ```

3. **Update search function** in `src/literature_search/cli.py`:
   ```python
   elif db_name == 'NewDB':
       return get_publications_newdb(keyword_list, api_key, page_size, logic)
   ```

4. **Add tests** in `tests/test_api_clients_new.py`

5. **Update documentation**:
   - `docs/databases.md`
   - `README.md`
   - `NEW_DATABASES.md`

## Testing Guidelines

### Writing Tests

- Use `pytest` for testing
- Aim for >80% code coverage
- Test both success and failure cases
- Mock external API calls
- Use descriptive test names

Example test:
```python
def test_load_config_valid_file():
    """Test loading a valid configuration file."""
    config = load_config('sample_input.json')
    assert 'initial_prisma_values' in config
    assert 'inclusion_criteria' in config['initial_prisma_values']
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_config_loader.py

# Run with coverage
pytest --cov=literature_search tests/
```

## Documentation Guidelines

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed. Explain what the function does,
    any important details, and edge cases.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input is provided
        APIError: When API call fails
        
    Examples:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Updating Documentation

When making changes:
- Update relevant `.md` files in `docs/`
- Update `README.md` if user-facing changes
- Update `CHANGELOG.md` with notable changes
- Keep code comments current

## Building and Publishing

### Building the Package

```bash
# Build the package
./build.sh build

# Build and test
./build.sh test

# Build, test, and publish
./build.sh publish
```

### Publishing to PyPI

The package is automatically published to PyPI when:
1. Changes are merged to the main branch, AND
2. The commit message starts with `[release]`

Example: `[release] Version 1.0.0 with new features`

The publication uses PyPI OIDC for secure authentication.

## Pull Request Checklist

Before submitting a pull request:

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] No API keys or secrets in code
- [ ] Changes are focused and minimal
- [ ] Backward compatibility maintained (or noted)
- [ ] CHANGELOG.md updated (for significant changes)

## Code Review Process

1. **Submission**: Create pull request with clear description
2. **Automated checks**: GitHub Actions runs tests automatically
3. **Review**: Maintainers review code and provide feedback
4. **Iteration**: Address feedback and update PR
5. **Approval**: Once approved, maintainers will merge
6. **Merge**: Changes are merged to main branch

## Getting Help

- **Issues**: Check [GitHub Issues](https://github.com/shanakaprageeth/literature_search/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Read the documentation thoroughly
- **Code**: Review existing code for examples

## Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0 (GPL-3.0).

---

**Thank you for contributing to the Literature Review Tool!**

See `.github/copilot-instructions.md` for additional coding standards and conventions.
