#!/bin/bash
# Copy README.md to docs/index.md and fix relative links

set -e

echo "Copying README.md to docs/index.md and fixing relative links..."

# Copy README to docs
cp README.md docs/index.md

# Fix relative links for GitHub Pages context
# When in docs/index.md, we're at the root of the site, so:
# - "../../" (going up to root) should become "./" (current directory is root)
# - "examples/basic_syntax.html" stays the same (already relative to docs/)

sed -i 's|\.\./\.\./|./|g' docs/index.md

echo "✓ README copied and links fixed"
