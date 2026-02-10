# GitHub Pages Setup Instructions

This repository is now configured for GitHub Pages deployment. To complete the setup, you need to enable GitHub Pages in the repository settings.

## Steps to Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/nokout/pygments-soul-lexer
2. Click on **Settings** (top menu)
3. In the left sidebar, click on **Pages** (under "Code and automation")
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions" (not "Deploy from a branch")
5. Save the settings

## What Happens Next

Once GitHub Pages is enabled and you merge this PR to the `main` branch:

1. The GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) will automatically run
2. It will deploy the contents of the `docs/` directory to GitHub Pages
3. Your site will be available at: https://nokout.github.io/pygments-soul-lexer/

## What's Included

The GitHub Pages site includes:

- **Landing page** (`docs/index.html`): A formatted version of the README with navigation
- **Live examples** (`docs/examples/*.html`): Four syntax-highlighted SOUL code examples
  - Basic Syntax
  - Database Operations
  - OOP Features
  - Text Blocks

## Testing Locally

To preview the site locally:

```bash
cd docs
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Future Updates

To update the GitHub Pages site:

1. Modify files in the `docs/` directory
2. Commit and push to the `main` branch
3. The workflow will automatically redeploy the site

## Troubleshooting

If the deployment fails:

1. Check the Actions tab for error messages
2. Ensure GitHub Pages is enabled with "GitHub Actions" as the source
3. Verify the workflow has the necessary permissions (already configured in the workflow file)
