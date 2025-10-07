# GitHub Pages Setup Instructions

This document provides step-by-step instructions for setting up GitHub Pages for the Literature Review Tool documentation.

## Prerequisites

- Repository owner or admin access to the GitHub repository
- Documentation files already committed to the `docs/` directory
- GitHub Actions workflow file (`.github/workflows/pages.yml`) in place

## Step-by-Step Setup

### 1. Enable GitHub Pages

1. **Navigate to Repository Settings**
   - Go to https://github.com/shanakaprageeth/literature_search
   - Click on **Settings** tab (requires admin access)

2. **Go to Pages Settings**
   - In the left sidebar, scroll down and click on **Pages**

3. **Configure Build and Deployment**
   - Under **Source**, select: **GitHub Actions**
   - This will use the workflow file at `.github/workflows/pages.yml`

4. **Save Changes**
   - The configuration is automatically saved

### 2. Configure Pages Permissions (If Using GitHub Actions)

1. **In Settings → Pages:**
   - Ensure "Build and deployment" source is set to **GitHub Actions**

2. **In Settings → Actions → General:**
   - Scroll to "Workflow permissions"
   - Ensure **Read and write permissions** is selected
   - Check **Allow GitHub Actions to create and approve pull requests**
   - Click **Save**

### 3. Trigger the First Deployment

Option A: **Manual Workflow Trigger**
1. Go to **Actions** tab
2. Click on **Deploy GitHub Pages** workflow in the left sidebar
3. Click **Run workflow** button
4. Select `main` branch
5. Click **Run workflow**

Option B: **Push to Main Branch**
1. Make a commit to the `docs/` directory
2. Push to the `main` branch
3. GitHub Actions will automatically trigger

### 4. Verify Deployment

1. **Check Workflow Status**
   - Go to **Actions** tab
   - You should see a "Deploy GitHub Pages" workflow running
   - Wait for it to complete (usually takes 1-2 minutes)
   - Ensure all steps show green checkmarks

2. **Access the Documentation**
   - After successful deployment, visit: https://shanakaprageeth.github.io/literature_search/
   - The site should display the documentation home page
   - Test navigation to other pages

3. **Check Pages Settings**
   - Go to **Settings → Pages**
   - Under "Your site is live at", you should see the URL
   - Status should show as **Active**

## Troubleshooting

### Workflow Fails

**Issue**: "Deploy GitHub Pages" workflow fails

**Solutions**:
1. Check the workflow logs in the Actions tab
2. Verify `docs/_config.yml` syntax is correct
3. Ensure all markdown files are valid
4. Check that permissions are correctly set (Settings → Actions → General)

### Site Not Found (404 Error)

**Issue**: Visiting the GitHub Pages URL shows 404 error

**Solutions**:
1. Wait a few minutes - initial deployment can take time
2. Check if workflow completed successfully
3. Verify source is set to "GitHub Actions" in Pages settings
4. Check repository visibility (should be public or have Pages enabled for private repos)

### Styles Not Loading

**Issue**: Site loads but looks unstyled

**Solutions**:
1. Check `docs/_config.yml` has correct `baseurl: /literature_search`
2. Clear browser cache
3. Verify all links use relative paths

### Changes Not Reflecting

**Issue**: Updated documentation not showing on the site

**Solutions**:
1. Ensure changes are committed and pushed to `main` branch
2. Check GitHub Actions workflow triggered and completed
3. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
4. Wait a few minutes for CDN to update

## Alternative Setup (Branch-based)

If you prefer to deploy from a branch instead of GitHub Actions:

1. **In Settings → Pages:**
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
   - Click **Save**

2. **Note**: This method doesn't require the GitHub Actions workflow but has fewer customization options.

## Updating Documentation

Once GitHub Pages is set up:

1. **Edit documentation files** in the `docs/` directory
2. **Commit changes** to a feature branch
3. **Create a pull request** to main
4. **Merge the PR** to main
5. **Automatic deployment**: GitHub Actions will automatically rebuild and deploy

## Custom Domain (Optional)

To use a custom domain:

1. **In Settings → Pages:**
   - Under "Custom domain", enter your domain (e.g., `docs.example.com`)
   - Click **Save**

2. **Configure DNS:**
   - Add CNAME record pointing to `shanakaprageeth.github.io`
   - Or add A records for GitHub's IP addresses

3. **Wait for DNS propagation** (can take up to 24 hours)

4. **Enable HTTPS:**
   - Check "Enforce HTTPS" in Pages settings (after DNS propagates)

## Maintenance

### Regular Tasks

- **Monitor workflow runs**: Check Actions tab for failures
- **Update dependencies**: Keep Jekyll theme updated if needed
- **Check broken links**: Periodically verify all links work
- **Review analytics**: Use Google Analytics if configured

### Updating Jekyll Configuration

To update Jekyll settings:

1. Edit `docs/_config.yml`
2. Commit and push to main
3. Wait for automatic redeployment
4. Verify changes on live site

## Additional Resources

- **GitHub Pages Documentation**: https://docs.github.com/en/pages
- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Cayman Theme**: https://github.com/pages-themes/cayman

## Support

If you encounter issues not covered here:

1. Check GitHub Actions logs for error details
2. Review GitHub Pages documentation
3. Open an issue on the repository
4. Contact repository maintainers

---

**Setup Date**: October 2024

**Documentation Version**: 1.0

**Last Updated**: October 2024
