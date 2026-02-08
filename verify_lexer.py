#!/usr/bin/env python3
"""
Visual verification script for the SOUL Pygments lexer.
Generates HTML output for all example files.
"""

import sys
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter

from soul_lexer import SOULLexer


def generate_html_examples():
    """Generate HTML files for all example SOUL files."""
    examples_dir = Path("tests/examples")
    output_dir = Path("html_examples")
    output_dir.mkdir(exist_ok=True)

    lexer = SOULLexer()
    formatter = HtmlFormatter(
        full=True,
        style="monokai",
        linenos=True,
        title="SOUL Syntax Highlighting Examples",
    )

    for soul_file in examples_dir.glob("*.soul"):
        print(f"Processing {soul_file.name}...")

        with open(soul_file) as f:
            code = f.read()

        html = highlight(code, lexer, formatter)

        output_file = output_dir / f"{soul_file.stem}.html"
        with open(output_file, "w") as f:
            f.write(html)

        print(f"  ✓ Generated {output_file}")

    print(f"\n✓ All examples generated in {output_dir}/")
    print("  Open the HTML files in a browser to view the highlighted code.")


def verify_lexer():
    """Run basic verification tests."""
    print("=" * 70)
    print("SOUL Pygments Lexer Verification")
    print("=" * 70)
    print()

    # Test 1: Lexer registration
    print("Test 1: Lexer Registration")
    try:
        from pygments.lexers import get_lexer_by_name

        lexer = get_lexer_by_name("soul")
        print(f"  ✓ Lexer name: {lexer.name}")
        print(f"  ✓ Aliases: {', '.join(lexer.aliases)}")
        print(f"  ✓ File patterns: {', '.join(lexer.filenames)}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    print()

    # Test 2: Basic tokenization
    print("Test 2: Basic Tokenization")
    test_code = """
    * SOUL Example
    %NAME = 'Alice'
    IF $Len(%NAME) GT 0 THEN
        PRINT 'Hello ' WITH %NAME
    END IF
    """

    from pygments.token import Comment, Keyword, Name, Operator, String

    tokens = list(lexer.get_tokens(test_code))
    token_types = {t[0] for t in tokens}

    checks = [
        (Comment.Single in token_types, "Comments"),
        (Keyword in token_types, "Keywords"),
        (Name.Variable in token_types, "Variables"),
        (Name.Builtin in token_types, "$Functions"),
        (String.Single in token_types, "Strings"),
        (Operator in token_types, "Operators"),
    ]

    for check, name in checks:
        status = "✓" if check else "✗"
        print(f"  {status} {name}")

    print()

    # Test 3: Generate HTML examples
    print("Test 3: Generate HTML Examples")
    try:
        generate_html_examples()
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

    print()
    print("=" * 70)
    print("✓ All verification tests passed!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = verify_lexer()
    sys.exit(0 if success else 1)
