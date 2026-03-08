# Pygments SOUL Lexer

A [Pygments](https://pygments.org/) lexer for **SOUL** (System Online User Language), the 4GL language for Rocket Software's Model 204 database system.

## Examples

Interactive HTML examples with syntax highlighting:
- [Basic Syntax](examples/basic_syntax.html) - Variables, control flow
- [Database Operations](examples/database_ops.html) - FIND, STORE, UPDATE, DELETE
- [OOP Features](examples/oop_features.html) - Classes, methods, inheritance
- [Text Blocks](examples/text_blocks.html) - TEXT/HTML interpolation

Source files available in `tests/examples/`.

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



## GitHub Pages

The project site is built with Jekyll and deployed automatically on push to `main`.

**Prerequisites:** Ruby >= 3.0, Bundler (`gem install bundler`), and the package installed in dev mode (`pip install -e ".[dev]"`).

**One-shot build** (mirrors the GitHub Action exactly):

```bash
bash scripts/build_docs.sh
```

Output is written to `./_site/`. Use this to verify the build before pushing.

**Local server** (live-reloading, for reviewing and editing):

```bash
bash scripts/build_docs.sh --serve
```

Then open http://localhost:4000. The script runs `generate_examples.sh` and `copy_readme.sh` before each build, so the local output matches what the action produces.

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
