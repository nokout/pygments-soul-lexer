#!/bin/bash
# Build (or serve) the GitHub Pages site locally.
#
# Usage:
#   bash scripts/build_docs.sh          # one-shot build → ./_site/
#   bash scripts/build_docs.sh --serve  # build + serve at http://localhost:4000

set -e

SERVE=false
for arg in "$@"; do
    case "$arg" in
        --serve) SERVE=true ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

# --- Prerequisites ---
if ! command -v ruby &>/dev/null; then
    echo "Error: ruby is not installed. Install Ruby >= 3.0 and bundler." >&2
    exit 1
fi
if ! command -v bundle &>/dev/null; then
    echo "Error: bundler is not installed. Run: gem install bundler" >&2
    exit 1
fi
if ! command -v pygmentize &>/dev/null; then
    echo "Error: pygmentize is not installed. Run: pip install -e '.[dev]'" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- Install Ruby gems (matches github-pages env used by the action) ---
echo "Installing Ruby gems..."
BUNDLE_GEMFILE=docs/Gemfile bundle install --quiet

# --- Pre-processing (mirrors action steps) ---
echo "Generating HTML examples from SOUL files..."
bash scripts/generate_examples.sh

echo "Copying README to docs/index.md..."
bash scripts/copy_readme.sh

# --- Jekyll build or serve ---
if [ "$SERVE" = true ]; then
    echo ""
    echo "Starting Jekyll server at http://localhost:4000 ..."
    echo "Press Ctrl-C to stop."
    echo ""
    BUNDLE_GEMFILE=docs/Gemfile bundle exec jekyll serve \
        --source ./docs \
        --destination ./_site \
        --livereload
else
    echo "Building Jekyll site..."
    BUNDLE_GEMFILE=docs/Gemfile bundle exec jekyll build \
        --source ./docs \
        --destination ./_site
    echo ""
    echo "Done. Output in ./_site/"
fi
