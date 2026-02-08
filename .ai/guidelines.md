# Development Guidelines for AI Coding Assistants

## Project Context
This is a **Pygments lexer** for the **SOUL programming language**. Every change must maintain compatibility with Pygments' RegexLexer architecture and preserve existing functionality.

## Critical Rules

### 1. Always Run Tests
- **Before committing**: `pytest tests/ -v` must pass (94 tests)
- **After any lexer change**: Test affected token types
- **After formatting**: Verify no behavioral changes

### 2. Pattern Ordering Matters
In `lexer.py`, patterns are evaluated **in order**:
```python
# ✅ CORRECT - specific before general
(r"%[a-z_]\w*::[a-z_]\w*\(", ...),  # Most specific
(r"%[a-z_]\w*::[a-z_]\w*", ...),    # More specific  
(r"%%[a-z_]\w*", ...),              # Specific
(r"%[a-z_]\w*", ...),               # General - matches anything remaining
```

If you reverse this order, the general pattern will match first and specific patterns become unreachable.

### 3. Regex Patterns - Common Pitfalls

**Word Boundaries**: Use `\b` to prevent partial matches
```python
(r"\bFIND\b", Keyword)  # ✅ Matches "FIND" not "FIND1"
(r"FIND", Keyword)      # ❌ Would match "FIND1", "FINDING"
```

**Multi-word Keywords**: Use `[ \t]+` not `\s+`
```python
(r"\b(FOR[ \t]+EACH[ \t]+RECORD)\b", Keyword)  # ✅ Single line only
(r"\b(FOR\s+EACH\s+RECORD)\b", Keyword)        # ❌ Matches across newlines
```

**Lookahead in Text Blocks**: Required to not consume END markers
```python
(r"[^\{]+?(?=END[ \t]+TEXT|\{)", String)  # ✅ Stops before END TEXT
(r"[^\{]+", String)                        # ❌ Would consume END TEXT
```

### 4. State Machine Transitions
- `"#pop"` returns to previous state
- States can nest (e.g., interpolation in text-block)
- Always ensure every state has an exit path
- Test nested cases (e.g., `{%VAR}` inside TEXT blocks)

### 5. Token Type Selection
Use appropriate Pygments token types:
- `Keyword` - language keywords (IF, FOR, WHILE)
- `Keyword.Declaration` - declarations (CLASS, IMAGE, FUNCTION)
- `Keyword.Type` - type names (FIXED, FLOAT, STRING)
- `Name.Variable` - variables (%VAR)
- `Name.Variable.Global` - field variables (%%VAR)
- `Name.Builtin` - built-in functions ($FUNC)
- `Name.Function` - user functions/methods
- `Operator.Word` - word operators (AND, OR, NOT)
- `Comment.Preproc` - preprocessor (#DEF, #IFDEF)

### 6. Testing Best Practices

**Parametrize Instead of Loops**:
```python
# ✅ GOOD - each case is a separate test
@pytest.mark.parametrize("op", ["+", "-", "*", "/"])
def test_operator(lexer, op):
    tokens = get_tokens(lexer, op)
    assert tokens[0][0] == Operator

# ❌ BAD - all cases in one test, poor error reporting
def test_operators(lexer):
    for op in ["+", "-", "*", "/"]:
        tokens = get_tokens(lexer, op)
        assert tokens[0][0] == Operator
```

**Exact Token Assertions** (when possible):
```python
# ✅ GOOD - exact sequence verification
tokens = [t for t in get_tokens(lexer, "%VAR") if t[0] != Whitespace]
assert tokens == [(Name.Variable, "%VAR")]

# ❌ LOOSE - could pass with wrong tokens
token_types = [t[0] for t in tokens]
assert Name.Variable in token_types
```

### 7. Code Style - Ruff Configuration

The project uses **ruff** with strict rules:
- **Line length**: 100 characters
- **Quotes**: Double quotes for strings
- **Imports**: Sorted (isort)
- **Formatting**: Auto-formatted

**Before committing**:
```bash
ruff check --fix .  # Auto-fix issues
ruff format .       # Format code
pytest tests/ -v    # Verify tests pass
```

### 8. Commit Message Format

Use conventional commits:
```
type(scope): subject

body (optional)
footer (optional)
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Test changes
- `refactor`: Code restructuring
- `ci`: CI/CD changes
- `docs`: Documentation

**Example**:
```
feat: Add support for SUPER.CONSTRUCTOR syntax

- Add dot (.) to punctuation patterns
- Update both root and interpolation states
- Add test case for nested class constructors
- Addresses issue #2
```

## Common Scenarios

### Adding a New SOUL Keyword

1. **Identify the keyword type** (Keyword, Keyword.Declaration, Keyword.Type)
2. **Check if multi-word** (e.g., "FOR EACH RECORD")
3. **Add to appropriate group** in `lexer.py`:
   ```python
   # For multi-word
   (r"\b(NEW[ \t]+KEYWORD[ \t]+FORM)\b", Keyword),
   
   # For single-word
   words(("NEWKW", "OTHERKW"), prefix=r"\b", suffix=r"\b"),
   ```
4. **Add test**:
   ```python
   def test_new_keyword(self, lexer):
       tokens = self.get_tokens(lexer, "NEWKW")
       assert tokens[0][0] == Keyword
   ```
5. **Run tests**: `pytest tests/ -v`

### Fixing a Tokenization Bug

1. **Create a minimal test case** that reproduces the issue
2. **Run the test** to confirm it fails
3. **Debug with print statements**:
   ```python
   tokens = list(lexer.get_tokens("problematic code"))
   for token in tokens:
       print(token)
   ```
4. **Identify the problematic pattern** (check pattern order)
5. **Fix the pattern** (adjust regex, reorder, add lookahead)
6. **Verify the test passes**
7. **Check no regressions**: `pytest tests/ -v`

### Adding Support for New Syntax

Example: Adding support for `@decorator` syntax

1. **Research**: Understand the syntax in SOUL specification
2. **Choose token type**: `Name.Decorator` (or similar)
3. **Add pattern** to root state:
   ```python
   (r"@[a-z_]\w*", Name.Decorator),
   ```
4. **Add tests**:
   ```python
   def test_decorator(self, lexer):
       tokens = [t for t in self.get_tokens(lexer, "@decorator") 
                 if t[0] != Whitespace]
       assert tokens == [(Name.Decorator, "@decorator")]
   ```
5. **Create example file** in `tests/examples/decorators.soul`
6. **Run all tests**: `pytest tests/ -v`
7. **Update documentation** if user-facing

## Anti-Patterns to Avoid

### ❌ Don't Break Pattern Order
```python
# BAD - general pattern before specific
(r"%[a-z_]\w*", Name.Variable),           # Matches everything
(r"%[a-z_]\w*::[a-z_]\w*", Name.Function), # Never reached!
```

### ❌ Don't Use Overly Broad Patterns
```python
# BAD - matches too much
(r"[A-Z]+", Keyword)  # Would match all caps words

# GOOD - specific keyword list
words(("IF", "FOR", "WHILE"), prefix=r"\b", suffix=r"\b")
```

### ❌ Don't Forget Edge Cases
Always test:
- Empty inputs
- Unclosed blocks/strings
- Nested structures
- Windows line endings (`\r\n`)
- Multiple spaces in multi-word keywords

### ❌ Don't Ignore Whitespace Handling
```python
# Remember that "\n" is often emitted as a separate token
# Filter it in tests when checking exact sequences:
tokens = [t for t in get_tokens(lexer, code) if t[0] != Whitespace]
```

### ❌ Don't Modify Without Testing
Every change to `lexer.py` MUST be accompanied by:
1. Test that covers the new behavior
2. Verification that existing tests still pass
3. Linting check: `ruff check .`

## Performance Considerations

1. **Avoid catastrophic backtracking** in regex:
   - Use possessive quantifiers when possible
   - Limit nested quantifiers
   - Test with long inputs

2. **Pattern complexity**:
   - Simple patterns are faster
   - Lookaheads have overhead (but sometimes necessary)

3. **State transitions**:
   - Minimize state changes when possible
   - Each push/pop has a small cost

## Integration Testing

The `tests/examples/*.soul` files serve as integration tests:
- **basic_syntax.soul**: Core language features
- **database_ops.soul**: Database operations
- **oop_features.soul**: Object-oriented features
- **text_blocks.soul**: Text interpolation

When adding major features, update or add example files to ensure comprehensive integration testing.

## When in Doubt

1. **Check Pygments documentation**: http://pygments.org/docs/
2. **Look at similar lexers**: `pygments/lexers/*.py` in Pygments source
3. **Test thoroughly**: Edge cases are where bugs hide
4. **Ask for clarification**: Better to ask than to guess

## Quick Reference

**Run tests**: `pytest tests/ -v`  
**Fix linting**: `ruff check --fix .`  
**Format code**: `ruff format .`  
**Debug tokens**: `python -c "from soul_lexer import SOULLexer; print(list(SOULLexer().get_tokens('code')))"`  
**Generate examples**: `python verify_lexer.py`

---

Remember: **Test-driven development** is crucial. Write the test first, watch it fail, then implement the fix and watch it pass.
