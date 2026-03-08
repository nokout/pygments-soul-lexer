---
layout: default
title: Setup Instructions
---

# GitHub Pages Setup Instructions

This repository is configured for automated GitHub Pages deployment with auto-generated documentation.

## Steps to Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/nokout/pygments-soul-lexer
2. Click on **Settings** (top menu)
3. In the left sidebar, click on **Pages** (under "Code and automation")
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions" (not "Deploy from a branch")
5. Save the settings

## What Happens Automatically

Once GitHub Pages is enabled and you push to the `main` branch, the workflow automatically:

1. **Generates HTML examples** from SOUL source files in `tests/examples/` using `pygmentize`
2. **Copies README.md** to `docs/index.md` and fixes relative links for GitHub Pages
3. **Deploys to GitHub Pages** at https://nokout.github.io/pygments-soul-lexer/

This ensures the documentation always stays up-to-date with the latest code examples.

## What's Included

The GitHub Pages site includes:

- **Landing page** (`docs/index.md`): Auto-copied from README.md with fixed relative links (GitHub Pages renders markdown)
- **Live examples** (`docs/examples/*.html`): Auto-generated from `tests/examples/*.soul` files using `pygmentize`
  - Basic Syntax
  - Database Operations
  - OOP Features
  - Text Blocks

## Testing Locally

To preview the site locally:

```bash
# Install the lexer
pip install -e .

# Generate HTML examples
bash scripts/generate_examples.sh

# Copy README and fix links
bash scripts/copy_readme.sh

# Serve with Python (markdown won't render, but HTML examples will work)
cd docs
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

For full markdown rendering preview, you can use GitHub's `gh` CLI:
```bash
gh repo view --web
```

## Updating the Site

The site updates automatically when you:

1. Modify SOUL example files in `tests/examples/`
2. Update the README.md
3. Push changes to the `main` branch

The GitHub Actions workflow regenerates everything automatically.

## Manual Generation (Optional)

To manually regenerate the HTML examples locally:

```bash
bash scripts/generate_examples.sh
```

To manually copy and fix README links:

```bash
bash scripts/copy_readme.sh
```

These are useful for testing before pushing changes.

## Troubleshooting

If the deployment fails:

1. Check the Actions tab for error messages
2. Ensure GitHub Pages is enabled with "GitHub Actions" as the source
3. Verify the workflow has the necessary permissions (already configured)
4. Ensure the lexer is installed (`pip install -e .`) before running generation scripts
