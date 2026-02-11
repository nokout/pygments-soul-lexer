#!/bin/bash
# Copy README.md to docs/index.md and fix relative links

set -e

# Cleanup function
cleanup() {
    rm -f docs/index.md.tmp docs/index.md.tmp2
}

# Set up trap to cleanup on exit or error
trap cleanup EXIT

echo "Copying README.md to docs/index.md and fixing relative links..."

# Create temporary file with Jekyll front matter
cat > docs/index.md.tmp << 'EOF'
---
layout: default
title: Home
---

EOF

# Append README content
cat README.md >> docs/index.md.tmp

# Fix relative links for GitHub Pages context
# When in docs/index.md, we're at the root of the site, so:
# - "../../" (going up to root) should become "./" (current directory is root)
# - "examples/basic_syntax.html" stays the same (already relative to docs/)

# Use portable sed (works on both Linux and macOS)
sed 's|\.\./\.\./|./|g' docs/index.md.tmp > docs/index.md.tmp2
if ! mv docs/index.md.tmp2 docs/index.md; then
    echo "Error: Failed to update docs/index.md" >&2
    exit 1
fi

echo "✓ README copied, front matter added, and links fixed"
