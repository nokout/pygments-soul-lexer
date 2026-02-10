#!/usr/bin/env python3
"""Generate HTML examples from SOUL source files for GitHub Pages."""

import sys
from pathlib import Path
from pygments import highlight
from pygments.formatters import HtmlFormatter
from soul_lexer import SOULLexer


def generate_html_example(soul_file: Path, output_file: Path) -> None:
    """Generate HTML file with syntax highlighting from SOUL source."""
    print(f"Generating {output_file.name} from {soul_file.name}...")
    
    # Read SOUL source code
    code = soul_file.read_text(encoding='utf-8')
    
    # Generate HTML with syntax highlighting
    formatter = HtmlFormatter(
        full=True,
        style='monokai',
        title='SOUL Syntax Highlighting Examples',
        linenos=False
    )
    html = highlight(code, SOULLexer(), formatter)
    
    # Write output
    output_file.write_text(html, encoding='utf-8')
    print(f"  ✓ Generated {output_file}")


def main():
    """Generate all HTML examples."""
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Define paths
    examples_dir = project_root / 'tests' / 'examples'
    output_dir = project_root / 'docs' / 'examples'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all .soul files
    soul_files = sorted(examples_dir.glob('*.soul'))
    
    if not soul_files:
        print(f"Error: No .soul files found in {examples_dir}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(soul_files)} SOUL example files")
    print()
    
    # Generate HTML for each example
    for soul_file in soul_files:
        output_file = output_dir / f"{soul_file.stem}.html"
        generate_html_example(soul_file, output_file)
    
    print()
    print(f"✓ Successfully generated {len(soul_files)} HTML examples")


if __name__ == '__main__':
    main()
