#!/bin/bash
# Generate HTML examples from SOUL source files for GitHub Pages

set -e

# Configuration
TITLE="SOUL Syntax Highlighting Examples"
EXAMPLES_DIR="tests/examples"
OUTPUT_DIR="docs/examples"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Enable nullglob to handle case when no .soul files exist
shopt -s nullglob

# Find all .soul files
soul_files=("$EXAMPLES_DIR"/*.soul)

# Check if any .soul files were found
if [ ${#soul_files[@]} -eq 0 ]; then
    echo "Error: No .soul files found in $EXAMPLES_DIR" >&2
    exit 1
fi

echo "Generating HTML examples from SOUL files..."
echo

count=0
for soul_file in "${soul_files[@]}"; do
    filename=$(basename "$soul_file" .soul)
    output_file="$OUTPUT_DIR/${filename}.html"
    
    echo "Generating ${filename}.html from ${filename}.soul..."
    pygmentize -l soul -f html -O full,style=monokai,title="$TITLE" -o "$output_file" "$soul_file"
    echo "  ✓ Generated $output_file"
    
    count=$((count + 1))
done

echo
echo "✓ Successfully generated $count HTML examples"
