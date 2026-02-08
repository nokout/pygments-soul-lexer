# Plan: SOUL (System Online User Language) Pygments Lexer Plugin

## Context

This plan creates a Pygments syntax highlighting plugin for SOUL (System Online User Language), the 4GL programming language for Rocket Software's Model 204 database system. SOUL is a case-insensitive language with unique features including percent-prefixed variables, dollar-prefixed built-in functions, database operations, object-oriented programming, and text interpolation blocks.

There is currently no Pygments lexer for SOUL. Only a minimal VS Code extension exists that covers <5% of the language. This plugin will provide comprehensive syntax highlighting for use in documentation (Sphinx), code editors, and any tool using Pygments.

## Project Structure

```
pygments-soul-lexer/
├── pyproject.toml                  # Package config with Pygments entry point
├── README.md                       # Documentation
├── LICENSE                         # BSD-3-Clause license
├── soul_lexer/
│   ├── __init__.py                # Package init
│   └── lexer.py                   # Main SOULLexer implementation
├── tests/
│   ├── __init__.py
│   ├── test_soul_lexer.py         # Pytest unit tests
│   └── examples/
│       ├── basic_syntax.soul      # Test examples
│       ├── database_ops.soul
│       ├── oop_features.soul
│       └── text_blocks.soul
└── .gitignore
```

## Implementation Steps

### 1. Create Project Structure

Create the directory tree and initialize the package:
- Create `soul_lexer/` directory with `__init__.py`
- Create `tests/` and `tests/examples/` directories
- Create `.gitignore` for Python projects (venv/, *.pyc, __pycache__/, .pytest_cache/, *.egg-info/)

### 2. Write pyproject.toml

Package configuration using modern `pyproject.toml` format with hatchling build backend:
- Package name: `pygments-soul-lexer`
- Version: `0.1.0`
- Dependencies: `pygments>=2.15.0`
- Dev dependencies: `pytest>=7.0.0`, `pytest-cov>=4.0.0`
- **Critical**: Entry point `[project.entry-points."pygments.lexers"]` with `soul = "soul_lexer.lexer:SOULLexer"`
- Metadata: description, license (BSD-3-Clause), keywords, classifiers

### 3. Implement SOULLexer (soul_lexer/lexer.py)

Create RegexLexer subclass with:

**Class metadata:**
- `name = 'SOUL'`
- `aliases = ['soul', 'model204']`
- `filenames = ['*.soul', '*.m204', '*.proc']`
- `flags = re.IGNORECASE | re.MULTILINE`

**Token rules in 'root' state (ordered by specificity):**

1. **Whitespace and continuation**: `r'\s+'` → Whitespace, `r'-\s*\n'` → Whitespace (line continuation)

2. **Comments**:
   - Line comments: `r'^\s*\*.*$'` → Comment.Single
   - Block comments: `r'/\?'` → Comment.Multiline, transition to 'block-comment' state

3. **Macro directives**: `r'^(\s*)(!)(DEF|UNDEF|IFDEF|IFNDEF|ELSE|ENDIF|IF|THEN)\b'` → bygroups(Whitespace, Comment.Preproc, Comment.Preproc)

4. **Labels**: `r'^(\s*)([a-z_]\w*)(:)(\s)'` → bygroups(Whitespace, Name.Label, Punctuation, Whitespace)

5. **TEXT/HTML blocks**: `r'\b(TEXT)\b'` → Keyword, push 'text-block' state (similar for HTML)

6. **Strings**: `r"'"` → String.Single, push 'string' state

7. **Dummy strings**:
   - `r'\?\?[^\s]+'` → String.Interpol (??prompt)
   - `r'\?\$[^\s]+'` → String.Interpol (?$prompt)
   - `r'\?&[a-z_]\w*'` → String.Interpol (?&global)
   - `r'\?![a-z_]\w*'` → String.Interpol (?!macro_var)

8. **Numbers**:
   - Float: `r'[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?'` → Number.Float
   - Scientific: `r'[0-9]+[eE][+-]?[0-9]+'` → Number.Float
   - Integer: `r'[0-9]+'` → Number.Integer

9. **$Functions**: `r'\$[a-z_]\w*'` → Name.Builtin

10. **Variables** (most specific first):
    - Object method calls: `r'(%[a-z_]\w*)(:)([a-z_]\w*)(\()'` → bygroups(Name.Variable, Punctuation, Name.Function, Punctuation)
    - Image items: `r'(%[a-z_]\w*)(:)([a-z_]\w*)'` → bygroups(Name.Variable, Punctuation, Name.Attribute)
    - Field variables: `r'%%[a-z_]\w*'` → Name.Variable.Global
    - Regular variables: `r'%[a-z_]\w*'` → Name.Variable

11. **Multi-word keywords** (longest first to avoid partial matches):
    - `r'\b(FOR\s+EACH\s+RECORD)\b'` → Keyword
    - `r'\b(FOR\s+EACH\s+VALUE)\b'` → Keyword
    - `r'\b(FOR\s+EACH\s+OCCURRENCE)\b'` → Keyword
    - `r'\b(FIND\s+ALL\s+RECORDS)\b'` → Keyword
    - `r'\b(STORE\s+RECORD)\b'` → Keyword
    - `r'\b(UPDATE\s+RECORD)\b'` → Keyword
    - `r'\b(DELETE\s+RECORD)\b'` → Keyword
    - All END statements: `r'\b(END\s+IF)\b'`, `r'\b(END\s+FOR)\b'`, etc. → Keyword
    - `r'\b(VARIABLES\s+ARE)\b'` → Keyword.Declaration
    - `r'\b(REPEAT\s+WHILE)\b'` → Keyword
    - `r'\b(REPEAT\s+UNTIL)\b'` → Keyword
    - `r'\b(IS\s+NOT\s+LIKE)\b'` → Operator.Word
    - `r'\b(IS\s+LIKE)\b'` → Operator.Word
    - `r'\b(IS\s+NOT\s+PRESENT)\b'` → Operator.Word
    - `r'\b(IS\s+PRESENT)\b'` → Operator.Word

12. **Keyword groups using words()**:
    - Declaration keywords: DECLARE, IMAGE, CLASS, ENUMERATION, PROCEDURE, FUNCTION, SUBROUTINE, PROPERTY, CONSTRUCTOR → Keyword.Declaration
    - Type keywords: FIXED, FLOAT, STRING, LEN, DP, ARRAY, INITIAL, UNDEFINED → Keyword.Type
    - Visibility: PUBLIC, PRIVATE, SHARED, STATIC → Keyword.Declaration
    - Control flow: IF, THEN, ELSE, ELSEIF, FOR, TO, FROM, BY, REPEAT, WHILE, UNTIL, BEGIN, END, CALL, RETURN, TRY, CATCH, THROW → Keyword
    - Database ops + abbreviations: FIND, STORE, UPDATE, DELETE, FD, FDR, FDV, FR, FRN, FRV, FEO, FPC, AAI, CH, CT, ST, PAI, NP → Keyword
    - Other: IN, PRINT, AUDIT, SKIP, LINES, NEW, IS, RECORDS, VALUE, OCCURRENCE → Keyword

13. **Word operators**: AND, OR, NOT, NOR, ANDIF, ORIF, EQ, NE, GT, LT, GE, LE, WITH, LIKE, PRESENT → Operator.Word

14. **Symbolic operators**: `r'[+\-*/=<>]'`, `r'<>'`, `r'>='`, `r'<='` → Operator

15. **Punctuation**: `r'[(),:\[\]]'` → Punctuation

16. **Identifiers**: `r'[a-z_]\w*'` → Name (catch-all)

**Additional states:**

- **'block-comment'**: Match until `\?/`, handle nested content
- **'string'**: Match `''` as escaped quote, `'` as terminator, content as String.Single
- **'text-block'**: Match `END TEXT` to pop, `\{` to push 'interpolation', plain text as String
- **'html-block'**: Match `END HTML` to pop, `\{` to push 'interpolation', plain text as String
- **'interpolation'**: Match `\}` to pop, include most root patterns for expressions inside braces

### 4. Write Comprehensive Tests (tests/test_soul_lexer.py)

Create pytest test class `TestSOULLexer` with tests for:
- Lexer metadata (name, aliases)
- Line comments (`* comment`)
- Block comments (`/? comment ?/`)
- Variables (`%VAR`, `%%FIELD`, `%IMG:ITEM`)
- $Functions (`$Len`, `$Substr`)
- Strings with escaped quotes (`'it''s'`)
- Case-insensitive keywords (IF/if/If all → Keyword)
- Multi-word keywords (FOR EACH RECORD as single token)
- Labels (`LOOP: FOR...`)
- Numbers (integer, float, scientific)
- Operators (symbolic and word forms)
- Macro directives (`!DEF`, `!IFDEF`)
- TEXT block interpolation (`{%VAR}`)
- Object method calls (`%OBJ:METHOD()`)
- Image item references (`%IMG:FIELD`)
- Line continuation (trailing hyphen)
- Parametrized test for all major keywords

Helper method: `get_tokens(lexer, text)` returns list of (token_type, value) tuples

### 5. Create Example Files (tests/examples/)

**basic_syntax.soul**: Variables, strings, IF/ELSE, PRINT statements
**database_ops.soul**: FIND ALL RECORDS, FOR EACH RECORD, STORE RECORD
**oop_features.soul**: CLASS definition, CONSTRUCTOR, FUNCTION, method calls
**text_blocks.soul**: TEXT/HTML blocks with expression interpolation

These serve as both test fixtures and documentation examples.

### 6. Write Documentation (README.md)

Include:
- What is SOUL (brief intro to Model 204 language)
- Installation: `pip install pygments-soul-lexer`
- Usage examples:
  - Command-line: `pygmentize -l soul myfile.soul`
  - Python API: `highlight(code, SOULLexer(), HtmlFormatter())`
  - Sphinx: `.. code-block:: soul`
- Supported features list
- Known limitations
- Contributing guidelines
- License (BSD-3-Clause)
- Links to M204 wiki documentation

### 7. Create LICENSE file

Use BSD-3-Clause license (compatible with Pygments and widely used for Pygments plugins)

### 8. Create .gitignore

Standard Python ignores:
```
venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
*.html
```

## Verification Steps

After implementation:

1. **Install in development mode**: `pip install -e .`
2. **Run tests**: `pytest tests/ -v --cov=soul_lexer`
3. **Visual test**: Create test script that outputs highlighted HTML for each example file
4. **Command-line test**: `pygmentize -l soul tests/examples/basic_syntax.soul`
5. **Verify entry point registration**: `python -c "from pygments.lexers import get_lexer_by_name; print(get_lexer_by_name('soul'))"`
6. **Check all token types**: Ensure no Error tokens on valid SOUL code
7. **Round-trip test**: Verify all input characters appear in tokenized output

## Critical Files

1. **soul_lexer/lexer.py** - Core lexer with 400+ lines of regex patterns, state machine logic
2. **pyproject.toml** - Package config with Pygments entry point registration
3. **tests/test_soul_lexer.py** - Comprehensive test suite (20+ test methods)
4. **tests/examples/basic_syntax.soul** - Primary example file demonstrating core syntax
5. **README.md** - User documentation with installation and usage examples

## Edge Cases Handled

1. **Multi-word keyword ordering**: Longest patterns first (FOR EACH RECORD before FOR)
2. **Colon disambiguation**: Check for `(` to distinguish `%OBJ:METHOD()` from `%IMG:ITEM`
3. **Labels vs keywords**: Labels only match at line start with `^(\s*)`
4. **Line continuation**: Trailing hyphen treated as whitespace, not operator
5. **TEXT/HTML interpolation**: State-based parsing with expression support inside `{...}`
6. **Case insensitivity**: `re.IGNORECASE` flag handles all keyword variations
7. **Comment detection**: `*` must be first non-blank character on line
8. **Escaped quotes**: `''` within strings handled in string state
9. **Block comment nesting**: Not currently supported (SOUL doesn't require it)

## Future Enhancements (Post v0.1.0)

- Validate $Function names against complete list of 300+ built-in functions
- Context-aware highlighting (track whether inside CLASS, IMAGE, etc.)
- Support for all SOUL statement abbreviations
- Custom color scheme optimized for SOUL syntax
- Language server integration for semantic highlighting
- Documentation site with interactive examples
