# Documentation

This directory contains the GitHub Pages documentation for the Literature Review Tool.

## Live Documentation

Visit the live documentation at: **https://shanakaprageeth.github.io/literature_search/**

## Local Preview

To preview the documentation locally:

1. Install Jekyll:
   ```bash
   gem install bundler jekyll
   ```

2. Navigate to the docs directory:
   ```bash
   cd docs
   ```

3. Serve the documentation:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to: http://localhost:4000/literature_search/

## Documentation Files

- **index.md** - Home page
- **installation.md** - Installation guide
- **usage.md** - Usage guide
- **configuration.md** - Configuration guide
- **databases.md** - Database documentation
- **contributing.md** - Contribution guidelines
- **faq.md** - Frequently asked questions
- **MAINTAINING_DOCS.md** - Documentation maintenance guide

## Updating Documentation

See [MAINTAINING_DOCS.md](MAINTAINING_DOCS.md) for detailed instructions on maintaining and updating the documentation.

## Building and Deployment

Documentation is automatically built and deployed via GitHub Actions when changes are pushed to the `main` branch.

**Workflow:** `.github/workflows/pages.yml`

## Contributing

To contribute to the documentation:

1. Fork the repository
2. Create a branch for your changes
3. Edit the relevant `.md` files in the `docs/` directory
4. Test locally if possible
5. Submit a pull request

See [contributing.md](contributing.md) for detailed contribution guidelines.
