#!/bin/bash
# Generate HTML examples from SOUL source files for GitHub Pages

set -e

# Define paths
EXAMPLES_DIR="tests/examples"
OUTPUT_DIR="docs/examples"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Find all .soul files and generate HTML
echo "Generating HTML examples from SOUL files..."
echo

count=0
for soul_file in "$EXAMPLES_DIR"/*.soul; do
    if [ -f "$soul_file" ]; then
        filename=$(basename "$soul_file" .soul)
        output_file="$OUTPUT_DIR/${filename}.html"
        
        echo "Generating ${filename}.html from ${filename}.soul..."
        pygmentize -l soul -f html -O full,style=monokai,title="SOUL Syntax Highlighting Examples" -o "$output_file" "$soul_file"
        echo "  ✓ Generated $output_file"
        
        count=$((count + 1))
    fi
done

echo
echo "✓ Successfully generated $count HTML examples"
