# Documentation Maintenance Guide

This guide explains how to maintain and update the GitHub Pages documentation for the Literature Review Tool.

## Documentation Structure

The documentation is organized in the `docs/` directory:

```
docs/
├── _config.yml           # Jekyll configuration
├── index.md             # Home page
├── installation.md      # Installation guide
├── usage.md            # Usage guide
├── configuration.md    # Configuration guide
├── databases.md        # Database documentation
├── contributing.md     # Contribution guidelines
├── faq.md              # Frequently asked questions
└── MAINTAINING_DOCS.md # This file
```

## GitHub Pages Setup

### Initial Configuration

GitHub Pages is configured to build from the `docs/` directory on the `main` branch.

**To enable GitHub Pages:**

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/docs`
3. Click Save

The site will be available at: `https://shanakaprageeth.github.io/literature_search/`

### Automated Deployment

A GitHub Actions workflow (`.github/workflows/pages.yml`) automatically deploys documentation when:
- Changes are pushed to the `main` branch in the `docs/` directory
- The workflow is manually triggered

**Workflow file:** `.github/workflows/pages.yml`

## Updating Documentation

### Using GitHub Web Interface

For quick edits:

1. Navigate to the file in GitHub
2. Click the pencil (Edit) icon
3. Make your changes
4. Commit directly to main or create a pull request
5. GitHub Pages will rebuild automatically

### Using Git Locally

For more extensive changes:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shanakaprageeth/literature_search.git
   cd literature_search
   ```

2. **Create a branch:**
   ```bash
   git checkout -b docs/update-description
   ```

3. **Edit documentation files:**
   ```bash
   # Edit files in docs/ directory
   nano docs/installation.md
   ```

4. **Preview locally (optional):**
   ```bash
   # Install Jekyll (if not installed)
   gem install bundler jekyll
   
   # Serve documentation locally
   cd docs
   bundle exec jekyll serve
   
   # View at http://localhost:4000/literature_search/
   ```

5. **Commit and push:**
   ```bash
   git add docs/
   git commit -m "docs: Update installation instructions"
   git push origin docs/update-description
   ```

6. **Create pull request** on GitHub

7. **Merge to main** - GitHub Pages will rebuild automatically

### Using Copilot Agent

You can use GitHub Copilot to help update documentation:

1. **Open GitHub Copilot chat** in your editor
2. **Describe the update** you want to make
3. **Review suggestions** and apply them
4. **Commit changes** as described above

**Example prompts:**
- "Update the installation.md to include instructions for Python 3.11"
- "Add a new section to faq.md about handling SSL errors"
- "Improve the contributing.md with more detailed examples"

## Documentation Best Practices

### Writing Style

- **Clear and concise**: Use simple language
- **Consistent formatting**: Follow existing patterns
- **Code examples**: Include working examples
- **Screenshots**: Add screenshots for visual steps (if applicable)
- **Links**: Use relative links for internal pages
- **Headings**: Use proper heading hierarchy (H1, H2, H3)

### Markdown Guidelines

```markdown
# Main Title (H1) - Use once per page

## Section (H2) - Main sections

### Subsection (H3) - Subsections

#### Sub-subsection (H4) - When needed

**Bold text** for emphasis
*Italic text* for subtle emphasis
`inline code` for code snippets

```python
# Code blocks with syntax highlighting
def example():
    pass
```

[Link text](url) for hyperlinks
![Alt text](image-url) for images
```

### Code Examples

Always include:
- Syntax highlighting (```python, ```bash, ```json)
- Complete, working examples
- Comments explaining complex parts
- Expected output (when helpful)

### Internal Links

Use relative links for consistency:

```markdown
See the [Installation Guide](installation.md) for details.
See the [Configuration section](configuration.md#field-specific-criteria) for specifics.
```

### External Links

Use full URLs for external resources:

```markdown
Visit [PyPI](https://pypi.org/project/literature-search/) for the package.
```

## Common Updates

### Adding a New Database

When a new database is added to the tool:

1. **Update `databases.md`:**
   - Add database to the overview table
   - Add detailed section with API key instructions
   - Update example configurations

2. **Update `configuration.md`:**
   - Add database to examples
   - Update supported databases list

3. **Update `index.md`:**
   - Update feature list if needed
   - Update supported databases count

4. **Update `faq.md`:**
   - Add common questions about the new database

### Updating Version Information

When releasing a new version:

1. **Update references** to version numbers
2. **Update screenshots** if UI changed
3. **Update examples** if API changed
4. **Update `installation.md`** if requirements changed

### Adding New Features

When adding new features:

1. **Update `usage.md`:**
   - Add usage examples
   - Update CLI arguments table if needed

2. **Update `configuration.md`:**
   - Add configuration options
   - Provide examples

3. **Update `index.md`:**
   - Add to feature list
   - Update quick start if needed

4. **Update `faq.md`:**
   - Add anticipated questions

### Fixing Issues

When fixing documentation issues:

1. **Verify the problem** exists
2. **Make the fix** in the relevant file
3. **Check related pages** for consistency
4. **Test links** are working
5. **Commit with clear message:** `"docs: Fix typo in installation guide"`

## Testing Documentation

### Before Committing

- [ ] Spell check all changed content
- [ ] Verify all links work (internal and external)
- [ ] Check code examples are correct
- [ ] Ensure consistent formatting
- [ ] Preview locally if possible

### After Deployment

- [ ] Visit the live site
- [ ] Navigate through all updated pages
- [ ] Verify navigation works
- [ ] Check mobile responsiveness
- [ ] Test all links on live site

## Markdown Preview

### In VS Code

1. Install "Markdown All in One" extension
2. Open a `.md` file
3. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
4. Preview updates live

### In GitHub

1. Navigate to the file on GitHub
2. Click "Preview" tab when editing
3. See rendered markdown

### Local Jekyll Server

```bash
cd docs
bundle exec jekyll serve --watch
# Visit http://localhost:4000/literature_search/
```

## Troubleshooting

### Pages not updating

1. Check GitHub Actions workflow status
2. Verify changes are in `main` branch
3. Check `docs/` directory has changes
4. Wait a few minutes for build/deploy
5. Clear browser cache

### Broken links

1. Use relative links for internal pages
2. Verify file names match exactly (case-sensitive)
3. Check for typos in URLs
4. Test on live site after deployment

### Formatting issues

1. Verify markdown syntax
2. Check heading hierarchy
3. Ensure code blocks have closing backticks
4. Validate YAML in `_config.yml`

### Jekyll build failures

1. Check GitHub Actions logs
2. Validate `_config.yml` syntax
3. Ensure markdown is valid
4. Check for unsupported Jekyll features

## Quick Reference

### File Purposes

| File | Purpose |
|------|---------|
| `index.md` | Home page, project overview |
| `installation.md` | Installation instructions |
| `usage.md` | How to use the tool |
| `configuration.md` | Configuration file format |
| `databases.md` | Database-specific information |
| `contributing.md` | Contribution guidelines |
| `faq.md` | Common questions and answers |
| `_config.yml` | Jekyll configuration |

### Common Tasks

| Task | Command/Action |
|------|----------------|
| Preview locally | `bundle exec jekyll serve` in `docs/` |
| Edit file | Open `.md` file in text editor |
| Add new page | Create new `.md` file in `docs/` |
| Update navigation | Edit `_config.yml` |
| Deploy | Merge to `main` branch |

### Useful Commands

```bash
# Preview documentation locally
cd docs && bundle exec jekyll serve

# Check for broken links (requires linkchecker)
linkchecker http://localhost:4000/literature_search/

# Search documentation
grep -r "search term" docs/

# List all markdown files
find docs/ -name "*.md"
```

## Resources

- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **GitHub Pages Documentation**: https://docs.github.com/en/pages
- **Markdown Guide**: https://www.markdownguide.org/
- **GitHub Actions**: https://docs.github.com/en/actions

## Getting Help

If you need help with documentation:

1. Check this guide
2. Review existing documentation files for examples
3. Check GitHub Pages documentation
4. Open an issue on GitHub
5. Ask in GitHub Discussions

---

**Last Updated**: October 2024

**Maintained by**: Project contributors and maintainers
