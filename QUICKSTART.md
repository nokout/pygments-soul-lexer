# Quick Start Guide - SOUL Pygments Lexer

## Installation

### From Source (Development)

```bash
# Clone or navigate to the project directory
cd pygments-soul-lexer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### From PyPI (Once Published)

```bash
pip install pygments-soul-lexer
```

## Verify Installation

```bash
# Check if the lexer is registered
python -c "from pygments.lexers import get_lexer_by_name; print(get_lexer_by_name('soul'))"
```

Should output: `<pygments.lexers.SOULLexer>`

## Usage Examples

### 1. Command Line - Highlight to Terminal

```bash
# Syntax highlight a SOUL file with color output
pygmentize -l soul tests/examples/basic_syntax.soul

# Highlight with line numbers
pygmentize -l soul -O linenos=1 tests/examples/basic_syntax.soul
```

### 2. Command Line - Generate HTML

```bash
# Generate standalone HTML file with styling
pygmentize -l soul -f html -O full,style=monokai -o output.html myfile.soul

# Generate HTML fragment (for embedding)
pygmentize -l soul -f html myfile.soul > fragment.html
```

### 3. Python API - Basic Usage

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter, TerminalFormatter
from soul_lexer import SOULLexer

# Your SOUL code
code = """
* SOUL Example
%NAME = 'Alice'
IF $Len(%NAME) GT 0 THEN
    PRINT 'Hello, ' WITH %NAME
END IF
"""

# Highlight to terminal with colors
print(highlight(code, SOULLexer(), TerminalFormatter()))

# Generate HTML
html = highlight(code, SOULLexer(), HtmlFormatter(style='monokai'))
print(html)
```

### 4. Python API - Generate Complete HTML Page

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter
from soul_lexer import SOULLexer

with open('myfile.soul', 'r') as f:
    code = f.read()

formatter = HtmlFormatter(
    full=True,              # Generate complete HTML page
    style='monokai',        # Color scheme
    linenos=True,           # Show line numbers
    title='SOUL Code',      # Page title
)

html = highlight(code, SOULLexer(), formatter)

with open('output.html', 'w') as f:
    f.write(html)
```

### 5. Sphinx Documentation

In your `conf.py`:

```python
# No special configuration needed - lexer auto-discovered via entry point
```

In your `.rst` files:

```rst
.. code-block:: soul

   * Database query example
   FIND ALL RECORDS IN EMPLOYEES WHERE
       DEPT = 'SALES' AND
       SALARY GT 50000
   END FIND

   FOR EACH RECORD
       PRINT %%NAME WITH %%SALARY
   END FOR
```

### 6. Using with reStructuredText

```rst
SOUL Code Example
=================

Here's a simple SOUL program:

.. code-block:: soul
   :linenos:

   * Simple SOUL program
   %COUNT = 0
   FOR %I FROM 1 TO 10
       %COUNT = %COUNT + %I
   END FOR
   PRINT 'Sum: ' WITH %COUNT
```

### 7. Jupyter Notebook

```python
from IPython.display import HTML
from pygments import highlight
from pygments.formatters import HtmlFormatter
from soul_lexer import SOULLexer

code = """
FOR %I FROM 1 TO 10
    PRINT %I
END FOR
"""

formatter = HtmlFormatter(noclasses=True, style='monokai')
html = highlight(code, SOULLexer(), formatter)
display(HTML(html))
```

## Testing

### Run All Tests

```bash
# Run tests with coverage report
pytest tests/ -v --cov=soul_lexer --cov-report=term

# Generate HTML coverage report
pytest tests/ --cov=soul_lexer --cov-report=html
# Open htmlcov/index.html in browser
```

### Run Specific Tests

```bash
# Run a single test
pytest tests/test_soul_lexer.py::TestSOULLexer::test_variable_simple -v

# Run tests matching a pattern
pytest tests/ -k "keyword" -v
```

## Visual Verification

Run the included verification script to generate HTML examples:

```bash
python verify_lexer.py
```

This will:
1. Verify lexer registration
2. Test basic tokenization
3. Generate HTML files for all example SOUL files in `html_examples/`

Open the generated HTML files in a browser to see the syntax highlighting in action.

## Example Files

The `tests/examples/` directory contains comprehensive SOUL examples:

- **basic_syntax.soul** - Variables, strings, control flow, arithmetic
- **database_ops.soul** - FIND, STORE, UPDATE, DELETE operations
- **oop_features.soul** - Classes, objects, methods, inheritance
- **text_blocks.soul** - TEXT/HTML blocks with variable interpolation

## Supported Color Schemes

Pygments supports many built-in styles. Try different ones:

```python
from pygments.styles import get_all_styles

# List all available styles
print(list(get_all_styles()))

# Popular styles for SOUL code:
# - monokai (dark, high contrast)
# - github-dark (GitHub's dark theme)
# - dracula (popular dark theme)
# - vs (Visual Studio light)
# - friendly (light, readable)
```

## Common Issues

### Issue: `ModuleNotFoundError: No module named 'soul_lexer'`

**Solution**: Install the package first:
```bash
pip install -e .
```

### Issue: Lexer not found by Pygments

**Solution**: Reinstall to register the entry point:
```bash
pip install --force-reinstall -e .
```

### Issue: HTML output has no colors

**Solution**: Use `noclasses=True` in formatter or include CSS:
```python
# Option 1: Inline styles
formatter = HtmlFormatter(noclasses=True)

# Option 2: Generate CSS separately
css = HtmlFormatter(style='monokai').get_style_defs('.highlight')
```

## Language Features Covered

The lexer recognizes all major SOUL language features:

- ✅ Comments (line and block)
- ✅ Variables (%VAR, %%FIELD)
- ✅ $Functions ($Len, $Substr, etc.)
- ✅ Keywords (IF, FOR, FIND, STORE, etc.)
- ✅ Multi-word keywords (FOR EACH RECORD, END IF)
- ✅ Strings with escaped quotes
- ✅ Numbers (integer, float, scientific notation)
- ✅ Operators (symbolic and word forms)
- ✅ Database operations
- ✅ Object-oriented features
- ✅ TEXT/HTML blocks with interpolation
- ✅ Labels and macro directives
- ✅ Case-insensitive syntax

## Getting Help

- **README.md** - Comprehensive documentation
- **PLAN.md** - Implementation details and design decisions
- **tests/test_soul_lexer.py** - Usage examples in test cases
- **tests/examples/** - Real-world SOUL code examples

## Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass: `pytest tests/ -v`
6. Submit a pull request

## Next Steps

1. Try highlighting the example files
2. Run the verification script
3. Integrate into your documentation system
4. Customize color schemes for your needs
5. Provide feedback or contribute improvements!

Happy SOUL coding! 🚀
