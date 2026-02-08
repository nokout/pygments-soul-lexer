# Pygments SOUL Lexer Project

## Project Overview
This project provides a Pygments lexer for SOUL (System Online User Language), the 4GL programming language for Rocket Software's Model 204 database system. The lexer enables syntax highlighting for SOUL code in various tools and documentation systems that support Pygments.

## Project Structure

```
pygments-soul-lexer/
├── soul_lexer/              # Main package
│   ├── __init__.py         # Package initialization, version management
│   └── lexer.py            # Core lexer implementation (RegexLexer)
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_soul_lexer.py  # 94 comprehensive tests
│   └── examples/           # Integration test files
│       ├── basic_syntax.soul
│       ├── database_ops.soul
│       ├── oop_features.soul
│       └── text_blocks.soul
├── html_examples/          # Generated HTML examples (not tracked)
├── .github/
│   └── workflows/
│       └── lint.yml        # GitHub Actions: ruff linting
├── pyproject.toml          # Project configuration, dependencies, ruff config
├── README.md              # User documentation
├── PEER_REVIEW.md         # Comprehensive code review (Feb 2026)
├── IMPLEMENTATION_SUMMARY.md
├── PLAN.md
├── PUBLICATION_GUIDE.md
├── PYPI_CHECKLIST.md
└── verify_lexer.py        # Manual verification script
```

## Key Technologies

- **Python**: >=3.8
- **Pygments**: >=2.15.0,<3.0.0 (syntax highlighting framework)
- **pytest**: Test framework
- **ruff**: Linting and formatting
- **GitHub Actions**: CI/CD

## SOUL Language Features

The lexer supports:
- **Comments**: Line comments (`* comment`) and block comments (`/? comment ?/`)
- **Variables**: `%VAR` (local), `%%VAR` (field), `$FUNC` (built-in functions)
- **Keywords**: Case-insensitive, multi-word keywords (e.g., `FOR EACH RECORD`)
- **Operators**: Symbolic (`+`, `-`, `<>`) and word operators (`AND`, `OR`, `EQ`)
- **OOP**: Classes, methods, properties, inheritance (`SUPER.CONSTRUCTOR`)
- **Text Blocks**: `TEXT...END TEXT` with interpolation `{%VAR}`
- **Database**: `FIND`, `STORE`, `UPDATE`, `DELETE` operations
- **Macro Directives**: `!DEF`, `!IFDEF`, etc.
- **String Interpolation**: Braces `{}` in text blocks

## Development Workflow

### Setup
```bash
# Clone and setup
git clone https://github.com/nokout/pygments-soul-lexer.git
cd pygments-soul-lexer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=soul_lexer --cov-report=html

# Run specific test
pytest tests/test_soul_lexer.py::TestSOULLexer::test_text_block_basic -v
```

### Linting & Formatting
```bash
# Check linting
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Check formatting without changes
ruff format --check .
```

### Manual Verification
```bash
# Generate HTML examples
python verify_lexer.py
# Opens html_examples/ with highlighted code
```

## Code Architecture

### Lexer Design (soul_lexer/lexer.py)

**Class**: `SOULLexer(RegexLexer)`
- **Inheritance**: Pygments `RegexLexer` - state machine-based tokenizer
- **Flags**: `re.IGNORECASE | re.MULTILINE` - case-insensitive keywords
- **Method**: `analyse_text(text)` - auto-detection confidence scoring (0.0-1.0)

**Token States**:
1. **root**: Main parsing state
   - Comments (line and block)
   - Keywords (single and multi-word)
   - Variables, operators, strings
   - Entry points to other states

2. **block-comment**: Multi-line comments `/? ... ?/`
3. **string**: Single-quoted strings with escape handling
4. **text-block**: TEXT blocks with interpolation support
5. **html-block**: HTML blocks with interpolation support
6. **interpolation**: Expression parsing inside `{...}` in text blocks

**Token Types** (from `pygments.token`):
- `Comment.Single`, `Comment.Multiline`, `Comment.Preproc`
- `Keyword`, `Keyword.Declaration`, `Keyword.Type`
- `Name`, `Name.Variable`, `Name.Variable.Global`, `Name.Builtin`, `Name.Function`, `Name.Attribute`, `Name.Label`
- `Number.Integer`, `Number.Float`
- `Operator`, `Operator.Word`
- `String`, `String.Single`, `String.Interpol`
- `Punctuation`, `Whitespace`

### Test Organization (tests/test_soul_lexer.py)

**Test Class**: `TestSOULLexer`
- **Fixture**: `lexer` - provides `SOULLexer()` instance
- **Helper**: `get_tokens(lexer, code)` - returns token list

**Test Categories** (94 tests total):
1. **Metadata**: Lexer name, aliases, filenames
2. **Comments**: Line comments, block comments, edge cases
3. **Variables**: Local, field, image items, object methods
4. **Strings**: Simple, escaped quotes, dummy strings
5. **Keywords**: Case-insensitive, multi-word, declarations, types
6. **Numbers**: Integer, float, scientific notation
7. **Operators**: Symbolic, word operators
8. **Text Blocks**: Basic, interpolation, edge cases
9. **Edge Cases**: Unclosed strings, empty blocks, Windows line endings
10. **Integration**: Parametrized tests for all example files

**Parametrized Tests**: Use `@pytest.mark.parametrize` for better failure reporting
- 40 operator tests (symbolic + word)
- 24 keyword tests (declaration, type, visibility, database)
- 4 example file integration tests

## Important Implementation Details

### Pattern Ordering
Patterns are evaluated in order - most specific patterns must come first:
- Multi-word keywords before single-word keywords
- Longer operators (`<=`, `>=`, `<>`) before shorter (`<`, `>`)
- Specific variables (`%VAR:METHOD(`) before general (`%VAR`)

### State Management
- `"#pop"` returns to previous state
- States can push/pop multiple levels (e.g., interpolation within text blocks)
- `include()` can be used to share patterns (noted in Issue #1 for future refactoring)

### Multi-word Keywords
- Use `[ \t]+` not `\s+` to keep keywords on single line
- Patterns like `FOR[ \t]+EACH[ \t]+RECORD` prevent matching across newlines

### Lookahead in Text Blocks
- Non-greedy patterns with lookahead prevent consuming END markers
- `[^\{]+?(?=END[ \t]+TEXT|\{)` stops before END TEXT or interpolation

## Known Issues & Future Work

**GitHub Issues** (created from peer review):
1. **Issue #1**: Refactor interpolation state to use `include()` mechanism
2. **Issue #2**: Handle `%%VAR:METHOD` pattern in method/attribute context
3. **Issue #3**: Improve macro directive tokenization (split `!` and keyword)
4. **Issue #4**: Tighten test assertions for exact token sequences

## Recent Changes (Feb 2026)

**Commits**:
1. Fix: Remove dead code from text-block/html-block states
2. Feat: Add analyse_text method for lexer auto-detection
3. Fix: Require multi-word keywords to be on single line
4. Refactor: Use importlib.metadata for version management
5. Test: Convert loop-based tests to pytest.mark.parametrize
6. Test: Add comprehensive edge case tests (11 new tests)
7. Feat: Add dot to punctuation and integration tests
8. Refactor: Minor style improvements to lexer
9. CI: Add GitHub Actions workflow for ruff linting

**Test Coverage**: Increased from 46 to 94 tests (204% increase)

## Configuration

### pyproject.toml Key Sections

**[project]**
- Entry point: `pygments.lexers` → `soul = "soul_lexer.lexer:SOULLexer"`
- Dependencies: `pygments>=2.15.0,<3.0.0`
- Dev dependencies: `pytest`, `pytest-cov`, `ruff`

**[tool.ruff]**
- Line length: 100
- Target: Python 3.8+
- Linting: E, W, F, I, N, UP, B, C4, SIM, Q
- Formatting: Double quotes, spaces, Unix line endings

**[tool.pytest.ini_options]**
- Test paths: `["tests"]`
- Options: `-v` (verbose)

## Common Tasks for AI Assistants

### Adding a New Token Type
1. Import token type from `pygments.token` in `lexer.py`
2. Add pattern to appropriate state in `tokens` dict
3. Consider pattern ordering (most specific first)
4. Add test case in `test_soul_lexer.py`
5. Run tests and verify

### Adding a New Keyword
1. Add to appropriate `words()` group in `root` state
2. Consider if it's multi-word (needs separate pattern)
3. Add test case
4. Update documentation if user-facing

### Debugging Token Issues
1. Use `verify_lexer.py` to generate HTML and visually inspect
2. Add debug code: `tokens = list(lexer.get_tokens(code)); print(tokens)`
3. Check pattern ordering - earlier patterns take precedence
4. Verify regex flags (IGNORECASE, MULTILINE)
5. Test with edge cases

### Running CI Locally
```bash
# Simulate GitHub Actions
ruff check .
ruff format --check .
pytest tests/ -v
```

## Contact & Contributing

- **Repository**: https://github.com/nokout/pygments-soul-lexer
- **Issues**: https://github.com/nokout/pygments-soul-lexer/issues
- **License**: MIT

When contributing:
1. All tests must pass: `pytest tests/ -v`
2. Code must be formatted: `ruff format .`
3. Linting must pass: `ruff check .`
4. Add tests for new features
5. Update documentation as needed
