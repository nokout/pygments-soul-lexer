# Pygments SOUL Lexer

A [Pygments](https://pygments.org/) lexer for **SOUL** (System Online User Language), the 4GL language for Rocket Software's Model 204 database system.

## Installation

```bash
pip install pygments-soul-lexer
```

Development installation:

```bash
git clone https://github.com/nokout/pygments-soul-lexer.git
cd pygments-soul-lexer
pip install -e ".[dev]"
```

## Quick Start

**Command line:**
```bash
pygmentize -l soul myfile.soul
pygmentize -l soul -f html -o output.html myfile.soul
```

**Python:**
```python
from pygments import highlight
from pygments.formatters import HtmlFormatter
from soul_lexer import SOULLexer

code = """
* SOUL Example
%NAME = 'Alice'
IF $Len(%NAME) GT 0 THEN
    PRINT 'Hello ' WITH %NAME
END IF
"""

html = highlight(code, SOULLexer(), HtmlFormatter())
```

**Sphinx:**
```rst
.. code-block:: soul

   FOR EACH RECORD IN EMPLOYEES
       PRINT %%NAME WITH %%SALARY
   END FOR
```

## Features

**Language Support:**
- Comments: `* line`, `/? block ?/`
- Variables: `%VAR`, `%%FIELD`, `%IMG:ITEM`, `%OBJ:METHOD()`
- Functions: `$Len`, `$Substr`, `$Curdate`
- Keywords: IF, FOR, WHILE, FIND, STORE, CLASS, etc.
- Multi-word: FOR EACH RECORD, END IF, STORE RECORD
- Strings with escapes: `'it''s'`
- Numbers: integers, floats, scientific notation
- Operators: `+`, `-`, `*`, `/`, AND, OR, EQ, GT
- TEXT/HTML blocks with interpolation: `{%VAR}`
- Macro directives: `!DEF`, `!IFDEF`
- Case-insensitive syntax

**Supported extensions:** `.soul`, `.m204`, `.proc`  
**Lexer aliases:** `soul`, `model204`

## Testing

```bash
pytest tests/ -v                    # Run tests
pytest tests/ --cov=soul_lexer      # With coverage
python verify_lexer.py              # Visual verification
```

**94 tests, 100% coverage**

## Examples

See `tests/examples/`:
- `basic_syntax.soul` - Variables, control flow
- `database_ops.soul` - FIND, STORE, UPDATE, DELETE
- `oop_features.soul` - Classes, methods, inheritance
- `text_blocks.soul` - TEXT/HTML interpolation

## Project Structure

```
pygments-soul-lexer/
├── soul_lexer/
│   ├── __init__.py         # Package with version
│   └── lexer.py            # SOULLexer implementation
├── tests/
│   ├── test_soul_lexer.py  # 94 tests
│   └── examples/*.soul     # Example files
├── pyproject.toml          # Package config
└── README.md
```

## About SOUL

SOUL is a powerful 4GL for the Model 204 database with:
- Percent-prefixed variables (`%VAR`, `%%FIELD`)
- Dollar-prefixed built-ins (`$Len`, `$Substr`)
- Database operations (FIND, STORE, UPDATE, DELETE)
- Object-oriented programming
- Text interpolation blocks
- Rich database integration

See [Model 204 Wiki](https://m204wiki.rocketsoftware.com/) for more.

## Contributing

1. Fork and create feature branch
2. Add tests for changes
3. Run test suite: `pytest tests/ -v`
4. Run linting: `ruff check . && ruff format .`
5. Submit pull request

See `.ai/guidelines.md` for detailed development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

## Links

- **PyPI:** https://pypi.org/project/pygments-soul-lexer/
- **GitHub:** https://github.com/nokout/pygments-soul-lexer
- **Pygments:** https://pygments.org/
- **Model 204 Wiki:** https://m204wiki.rocketsoftware.com/
