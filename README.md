# Pygments SOUL Lexer

A comprehensive [Pygments](https://pygments.org/) syntax highlighting lexer for **SOUL** (System Online User Language), the 4GL programming language for Rocket Software's Model 204 database system.

## What is SOUL?

SOUL is a powerful fourth-generation programming language used with the Model 204 database management system. It features:

- **Percent-prefixed variables** (`%VAR`, `%%FIELD`)
- **Dollar-prefixed built-in functions** (`$Len`, `$Substr`)
- **Database operations** (FIND, STORE, UPDATE, DELETE)
- **Object-oriented programming** (classes, methods, inheritance)
- **Text interpolation blocks** (TEXT/HTML with `{%VAR}` syntax)
- **Case-insensitive syntax**
- **Rich database integration** with field references and record processing

For more information, visit the [Model 204 Wiki](https://m204wiki.rocketsoftware.com/).

## Features

This lexer provides comprehensive syntax highlighting for:

- ✅ Line comments (`* comment`) and block comments (`/? comment ?/`)
- ✅ Keywords (IF, FOR, WHILE, FIND, STORE, etc.)
- ✅ Multi-word keywords (FOR EACH RECORD, END IF, STORE RECORD)
- ✅ Variables (`%VAR`) and field variables (`%%FIELD`)
- ✅ Image item references (`%IMG:ITEM`)
- ✅ Object method calls (`%OBJ:METHOD()`)
- ✅ Built-in $Functions (`$Len`, `$Substr`, `$Curdate`)
- ✅ String literals with escaped quotes (`'it''s'`)
- ✅ Dummy strings (`??prompt`, `?$input`, `?&global`, `?!macro`)
- ✅ Numbers (integers, floats, scientific notation)
- ✅ Operators (symbolic: `+`, `-`, `*`; word: AND, OR, EQ, GT)
- ✅ Labels (`LOOP:`)
- ✅ TEXT and HTML blocks with expression interpolation (`{%VAR}`)
- ✅ Macro directives (`!DEF`, `!IFDEF`, `!ENDIF`)
- ✅ Line continuation (trailing hyphen)
- ✅ Case-insensitive syntax

## Installation

Install from PyPI (once published):

```bash
pip install pygments-soul-lexer
```

Or install from source for development:

```bash
git clone https://github.com/nokout/pygments-soul-lexer.git
cd pygments-soul-lexer
pip install -e .
```

## Usage

### Command Line

Highlight a SOUL file and output to terminal:

```bash
pygmentize -l soul myfile.soul
```

Generate HTML output:

```bash
pygmentize -l soul -f html -o output.html myfile.soul
```

### Python API

```python
from pygments import highlight
from pygments.formatters import HtmlFormatter, TerminalFormatter
from soul_lexer import SOULLexer

code = """
* SOUL Example
%NAME = 'Alice'
IF $Len(%NAME) GT 0 THEN
    PRINT 'Hello ' WITH %NAME
END IF
"""

# Highlight to terminal
result = highlight(code, SOULLexer(), TerminalFormatter())
print(result)

# Generate HTML
html = highlight(code, SOULLexer(), HtmlFormatter(full=True))
with open('output.html', 'w') as f:
    f.write(html)
```

### Sphinx Documentation

Add SOUL syntax highlighting to your Sphinx documentation:

1. Install the lexer: `pip install pygments-soul-lexer`
2. Use in reStructuredText:

```rst
.. code-block:: soul

   * SOUL code example
   FOR EACH RECORD IN EMPLOYEES
       PRINT %%NAME WITH %%SALARY
   END FOR
```

The lexer will be automatically discovered via the Pygments plugin entry point.

### Jupyter Notebooks

```python
from IPython.display import HTML
from pygments import highlight
from pygments.formatters import HtmlFormatter
from soul_lexer import SOULLexer

code = "FOR %I FROM 1 TO 10\n    PRINT %I\nEND FOR"
html = highlight(code, SOULLexer(), HtmlFormatter(noclasses=True))
display(HTML(html))
```

## Supported File Extensions

The lexer recognizes the following file extensions:

- `.soul` - Standard SOUL files
- `.m204` - Model 204 procedure files
- `.proc` - Procedure files

## Aliases

You can refer to the lexer using these aliases:

- `soul`
- `model204`

## Examples

See the `tests/examples/` directory for comprehensive SOUL code examples:

- `basic_syntax.soul` - Variables, strings, control flow
- `database_ops.soul` - FIND, STORE, UPDATE, DELETE operations
- `oop_features.soul` - Classes, objects, methods, inheritance
- `text_blocks.soul` - TEXT/HTML blocks with interpolation

## Known Limitations

- Nested block comments are not currently supported (SOUL doesn't require them)
- $Function names are not validated against the complete list of 300+ built-ins
- Context-aware highlighting (tracking whether inside CLASS, IMAGE, etc.) is not implemented

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=soul_lexer --cov-report=html
```

### Project Structure

```
pygments-soul-lexer/
├── pyproject.toml           # Package configuration
├── README.md                # This file
├── LICENSE                  # BSD-3-Clause license
├── soul_lexer/
│   ├── __init__.py         # Package initialization
│   └── lexer.py            # Main SOULLexer implementation
└── tests/
    ├── test_soul_lexer.py  # Comprehensive test suite
    └── examples/           # Example SOUL files
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes and add tests
4. Run the test suite (`pytest`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [Pygments](https://pygments.org/) - The Python syntax highlighting library
- [Model 204 Wiki](https://m204wiki.rocketsoftware.com/) - Official Model 204 and SOUL documentation
- [Rocket Software](https://www.rocketsoftware.com/) - Publisher of Model 204

## Credits

Created by the SOUL Lexer Contributors.

Special thanks to the Pygments team for their excellent syntax highlighting library.

## Version History

- **0.1.0** (2025) - Initial release
  - Comprehensive SOUL syntax support
  - Multi-word keyword handling
  - TEXT/HTML block interpolation
  - Object-oriented features
  - Full test suite
