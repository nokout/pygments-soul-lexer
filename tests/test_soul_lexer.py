"""
Comprehensive test suite for the SOUL Pygments lexer.
"""

from glob import glob

import pytest
from pygments.token import (
    Comment,
    Error,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)

from soul_lexer.lexer import SOULLexer


class TestSOULLexer:
    """Test suite for SOULLexer."""

    @pytest.fixture
    def lexer(self):
        """Provide a SOULLexer instance."""
        return SOULLexer()

    def get_tokens(self, lexer, text):
        """Helper to get list of (token_type, value) tuples."""
        return list(lexer.get_tokens(text))

    def test_lexer_metadata(self, lexer):
        """Test lexer name and aliases."""
        assert lexer.name == "SOUL"
        assert "soul" in lexer.aliases
        assert "model204" in lexer.aliases

    def test_line_comment(self, lexer):
        """Test line comments starting with *."""
        tokens = self.get_tokens(lexer, "* This is a comment\n")
        assert tokens == [
            (Comment.Single, "* This is a comment"),
            (Whitespace, "\n"),
        ]

    def test_line_comment_with_indent(self, lexer):
        """Test indented line comments."""
        tokens = self.get_tokens(lexer, "    * Indented comment\n")
        assert tokens == [
            (Whitespace, "    "),
            (Comment.Single, "* Indented comment"),
            (Whitespace, "\n"),
        ]

    def test_block_comment(self, lexer):
        """Test block comments with /? ... ?/."""
        tokens = self.get_tokens(lexer, "/? This is a block comment ?/")
        assert tokens == [
            (Comment.Multiline, "/?"),
            (Comment.Multiline, " This is a block comment "),
            (Comment.Multiline, "?/"),
            (Whitespace, "\n"),
        ]

    def test_variable_simple(self, lexer):
        """Test simple percent-prefixed variables."""
        tokens = self.get_tokens(lexer, "%VAR")
        assert tokens == [
            (Name.Variable, "%VAR"),
            (Whitespace, "\n"),
        ]

    def test_variable_field(self, lexer):
        """Test field variables with double percent."""
        tokens = self.get_tokens(lexer, "%%FIELD")
        assert tokens == [
            (Name.Variable.Global, "%%FIELD"),
            (Whitespace, "\n"),
        ]

    def test_variable_image_item(self, lexer):
        """Test image item references %IMG:ITEM."""
        tokens = self.get_tokens(lexer, "%IMG:FIELD")
        assert tokens == [
            (Name.Variable, "%IMG"),
            (Punctuation, ":"),
            (Name.Attribute, "FIELD"),
            (Whitespace, "\n"),
        ]

    def test_variable_object_method(self, lexer):
        """Test object method calls %OBJ:METHOD(."""
        tokens = self.get_tokens(lexer, "%OBJ:METHOD(")
        assert tokens == [
            (Name.Variable, "%OBJ"),
            (Punctuation, ":"),
            (Name.Function, "METHOD"),
            (Punctuation, "("),
            (Whitespace, "\n"),
        ]

    def test_dollar_function(self, lexer):
        """Test $Functions (built-in functions)."""
        tokens = self.get_tokens(lexer, "$Len(%STR)")
        assert tokens == [
            (Name.Builtin, "$Len"),
            (Punctuation, "("),
            (Name.Variable, "%STR"),
            (Punctuation, ")"),
            (Whitespace, "\n"),
        ]

    def test_string_simple(self, lexer):
        """Test simple string literals."""
        tokens = self.get_tokens(lexer, "'Hello World'")
        assert tokens == [
            (String.Single, "'"),
            (String.Single, "Hello World"),
            (String.Single, "'"),
            (Whitespace, "\n"),
        ]

    def test_string_escaped_quote(self, lexer):
        """Test strings with escaped quotes ''."""
        tokens = self.get_tokens(lexer, "'It''s working'")
        assert tokens == [
            (String.Single, "'"),
            (String.Single, "It"),
            (String.Single, "''"),
            (String.Single, "s working"),
            (String.Single, "'"),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("keyword", ["IF", "if", "If", "iF"])
    def test_case_insensitive_keyword(self, lexer, keyword):
        """Test that keywords work regardless of case."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword, keyword),
            (Whitespace, "\n"),
        ]

    def test_multi_word_keyword_for_each_record(self, lexer):
        """Test multi-word keyword FOR EACH RECORD."""
        tokens = self.get_tokens(lexer, "FOR EACH RECORD")
        # Should be a single keyword token, not three separate tokens
        assert tokens == [
            (Keyword, "FOR EACH RECORD"),
            (Whitespace, "\n"),
        ]

    def test_multi_word_keyword_end_if(self, lexer):
        """Test multi-word keyword END IF."""
        tokens = self.get_tokens(lexer, "END IF")
        assert tokens == [
            (Keyword, "END IF"),
            (Whitespace, "\n"),
        ]

    def test_label(self, lexer):
        """Test label at start of line."""
        tokens = self.get_tokens(lexer, "LOOP: FOR %I FROM 1 TO 10")
        assert tokens == [
            (Name.Label, "LOOP"),
            (Punctuation, ":"),
            (Whitespace, " "),
            (Keyword, "FOR"),
            (Whitespace, " "),
            (Name.Variable, "%I"),
            (Whitespace, " "),
            (Keyword, "FROM"),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, " "),
            (Keyword, "TO"),
            (Whitespace, " "),
            (Number.Integer, "10"),
            (Whitespace, "\n"),
        ]

    def test_number_integer(self, lexer):
        """Test integer literals."""
        tokens = self.get_tokens(lexer, "12345")
        assert tokens == [
            (Number.Integer, "12345"),
            (Whitespace, "\n"),
        ]

    def test_number_float(self, lexer):
        """Test float literals."""
        tokens = self.get_tokens(lexer, "123.45")
        assert tokens == [
            (Number.Float, "123.45"),
            (Whitespace, "\n"),
        ]

    def test_number_scientific(self, lexer):
        """Test scientific notation."""
        tokens = self.get_tokens(lexer, "1.23E+10")
        assert tokens == [
            (Number.Float, "1.23E+10"),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("op", ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>"])
    def test_operator_symbolic(self, lexer, op):
        """Test symbolic operators."""
        tokens = self.get_tokens(lexer, op)
        assert tokens == [
            (Operator, op),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("op", ["AND", "OR", "NOT", "EQ", "NE", "GT", "LT"])
    def test_operator_word(self, lexer, op):
        """Test word operators."""
        tokens = self.get_tokens(lexer, op)
        assert tokens == [
            (Operator.Word, op),
            (Whitespace, "\n"),
        ]

    def test_macro_directive(self, lexer):
        """Test macro directives like !DEF."""
        tokens = self.get_tokens(lexer, "!DEF MACRO_NAME")
        assert tokens == [
            (Comment.Preproc, "!"),
            (Comment.Preproc, "DEF"),
            (Whitespace, " "),
            (Name, "MACRO_NAME"),
            (Whitespace, "\n"),
        ]

    def test_text_block_basic(self, lexer):
        """Test TEXT block."""
        code = "TEXT\nHello World\nEND TEXT"
        tokens = self.get_tokens(lexer, code)
        assert tokens == [
            (Keyword, "TEXT"),
            (String, "\nHello World\n"),
            (Keyword, "END TEXT"),
            (Whitespace, "\n"),
        ]

    def test_text_block_interpolation(self, lexer):
        """Test TEXT block with variable interpolation."""
        code = "TEXT\nHello {%NAME}\nEND TEXT"
        tokens = self.get_tokens(lexer, code)
        assert tokens == [
            (Keyword, "TEXT"),
            (String, "\nHello "),
            (Punctuation, "{"),
            (Name.Variable, "%NAME"),
            (Punctuation, "}"),
            (String, "\n"),
            (Keyword, "END TEXT"),
            (Whitespace, "\n"),
        ]

    def test_dummy_string_double_question(self, lexer):
        """Test dummy string ??prompt."""
        tokens = self.get_tokens(lexer, "??ENTER_NAME")
        assert tokens == [
            (String.Interpol, "??ENTER_NAME"),
            (Whitespace, "\n"),
        ]

    def test_dummy_string_dollar(self, lexer):
        """Test dummy string ?$prompt."""
        tokens = self.get_tokens(lexer, "?$ENTER_VALUE")
        assert tokens == [
            (String.Interpol, "?$ENTER_VALUE"),
            (Whitespace, "\n"),
        ]

    def test_dummy_string_ampersand(self, lexer):
        """Test dummy string ?&global."""
        tokens = self.get_tokens(lexer, "?&GLOBAL_VAR")
        assert tokens == [
            (String.Interpol, "?&GLOBAL_VAR"),
            (Whitespace, "\n"),
        ]

    def test_dummy_string_exclamation(self, lexer):
        """Test dummy string ?!macro."""
        tokens = self.get_tokens(lexer, "?!MACRO_VAR")
        assert tokens == [
            (String.Interpol, "?!MACRO_VAR"),
            (Whitespace, "\n"),
        ]

    def test_line_continuation(self, lexer):
        """Test line continuation with trailing hyphen."""
        tokens = self.get_tokens(lexer, "PRINT %VAR -\n + 1")
        assert tokens == [
            (Keyword, "PRINT"),
            (Whitespace, " "),
            (Name.Variable, "%VAR"),
            (Whitespace, " "),
            (Whitespace, "-\n"),  # Line continuation treated as whitespace
            (Whitespace, " "),
            (Operator, "+"),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("keyword", ["DECLARE", "IMAGE", "CLASS", "FUNCTION", "PROCEDURE"])
    def test_declaration_keyword(self, lexer, keyword):
        """Test declaration keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword.Declaration, keyword),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("keyword", ["FIXED", "FLOAT", "STRING", "ARRAY"])
    def test_type_keyword(self, lexer, keyword):
        """Test type keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword.Type, keyword),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("keyword", ["PUBLIC", "PRIVATE", "SHARED", "STATIC"])
    def test_visibility_keyword(self, lexer, keyword):
        """Test visibility keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword.Declaration, keyword),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize("keyword", ["FIND", "STORE", "UPDATE", "DELETE", "FDR", "FRN"])
    def test_database_keyword(self, lexer, keyword):
        """Test database operation keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword, keyword),
            (Whitespace, "\n"),
        ]

    @pytest.mark.parametrize(
        "keyword",
        [
            "IF",
            "THEN",
            "ELSE",
            "FOR",
            "REPEAT",
            "WHILE",
            "UNTIL",
            "END",
            "CALL",
            "RETURN",
        ],
    )
    def test_control_flow_keywords(self, lexer, keyword):
        """Test control flow keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens == [
            (Keyword, keyword),
            (Whitespace, "\n"),
        ]

    def test_complex_expression(self, lexer):
        """Test a complex expression with multiple token types."""
        code = "%RESULT = $Len(%NAME) + 10"
        tokens = self.get_tokens(lexer, code)
        assert tokens == [
            (Name.Variable, "%RESULT"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Name.Builtin, "$Len"),
            (Punctuation, "("),
            (Name.Variable, "%NAME"),
            (Punctuation, ")"),
            (Whitespace, " "),
            (Operator, "+"),
            (Whitespace, " "),
            (Number.Integer, "10"),
            (Whitespace, "\n"),
        ]

    def test_find_all_records_statement(self, lexer):
        """Test FIND ALL RECORDS as a single multi-word keyword."""
        tokens = self.get_tokens(lexer, "FIND ALL RECORDS IN FILE")
        assert tokens == [
            (Keyword, "FIND ALL RECORDS"),
            (Whitespace, " "),
            (Keyword, "IN"),
            (Whitespace, " "),
            (Name, "FILE"),
            (Whitespace, "\n"),
        ]

    def test_store_record_statement(self, lexer):
        """Test STORE RECORD as a single multi-word keyword."""
        tokens = self.get_tokens(lexer, "STORE RECORD")
        assert tokens == [
            (Keyword, "STORE RECORD"),
            (Whitespace, "\n"),
        ]

    def test_no_error_tokens(self, lexer):
        """Test that valid SOUL code produces no Error tokens."""
        code = """
        * Comment
        %VAR = $Len('test')
        IF %VAR GT 0 THEN
            PRINT %VAR
        END IF
        """
        tokens = self.get_tokens(lexer, code)

        error_tokens = [t for t in tokens if t[0] == Error]
        assert len(error_tokens) == 0

    def test_unclosed_string(self, lexer):
        """Test unclosed string gracefully handles EOF."""
        tokens = list(self.get_tokens(lexer, "'hello"))
        # Should not raise an error, just tokenize what it can
        assert any(t[0] in (String.Single, String) for t in tokens)

    def test_unclosed_text_block(self, lexer):
        """Test unclosed TEXT block doesn't error."""
        code = "TEXT\nHello World"
        tokens = list(self.get_tokens(lexer, code))
        # Should have TEXT keyword and string content
        assert (Keyword, "TEXT") in tokens
        assert any(t[0] == String for t in tokens)

    def test_empty_text_block(self, lexer):
        """Test empty TEXT block (edge case for lookahead patterns)."""
        code = "TEXT\nEND TEXT"
        tokens = self.get_tokens(lexer, code)
        assert tokens == [
            (Keyword, "TEXT"),
            (String, "\n"),
            (Keyword, "END TEXT"),
            (Whitespace, "\n"),
        ]

    def test_keyword_prefix_not_matched(self, lexer):
        """Test that FIND1 is not matched as FIND keyword."""
        tokens = self.get_tokens(lexer, "FIND1")
        # Should be Name, not Keyword (word boundary check)
        assert tokens == [
            (Name, "FIND1"),
            (Whitespace, "\n"),
        ]

    def test_end_text_outside_block(self, lexer):
        """Test END TEXT outside a TEXT block is handled."""
        tokens = self.get_tokens(lexer, "END TEXT")
        # Should be recognized as a keyword even in root state
        assert tokens == [
            (Keyword, "END TEXT"),
            (Whitespace, "\n"),
        ]

    def test_nested_interpolation(self, lexer):
        """Test nested braces in TEXT block interpolation."""
        code = "TEXT\n{%VAR}\nEND TEXT"
        tokens = list(self.get_tokens(lexer, code))
        assert tokens == [
            (Keyword, "TEXT"),
            (String, "\n"),
            (Punctuation, "{"),
            (Name.Variable, "%VAR"),
            (Punctuation, "}"),
            (String, "\n"),
            (Keyword, "END TEXT"),
            (Whitespace, "\n"),
        ]

    def test_windows_line_endings(self, lexer):
        """Test Windows \\r\\n line endings work correctly."""
        code = "* Comment\r\n%VAR = 1\r\n"
        tokens = list(self.get_tokens(lexer, code))
        # The lexer normalizes \r\n to \n
        assert tokens == [
            (Comment.Single, "* Comment"),
            (Whitespace, "\n"),
            (Name.Variable, "%VAR"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, "\n"),
        ]

    def test_empty_comment(self, lexer):
        """Test comment with only asterisk and space."""
        tokens = self.get_tokens(lexer, "* ")
        assert tokens == [
            (Comment.Single, "* "),
            (Whitespace, "\n"),
        ]

    def test_comment_after_blank_lines(self, lexer):
        """Test comment recognition after multiple blank lines."""
        code = "\n\n    * This is a comment"
        tokens = self.get_tokens(lexer, code)
        # Leading newlines are consumed by the comment pattern
        assert tokens == [
            (Whitespace, "    "),
            (Comment.Single, "* This is a comment"),
            (Whitespace, "\n"),
        ]

    def test_multi_word_keyword_extra_spaces(self, lexer):
        """Test multi-word keyword with extra spaces."""
        tokens = self.get_tokens(lexer, "FOR  EACH  RECORD")
        # Should still match as keyword (uses [ \\t]+ pattern)
        assert tokens == [
            (Keyword, "FOR  EACH  RECORD"),
            (Whitespace, "\n"),
        ]

    def test_label_keyword_name(self, lexer):
        """Test label that matches keyword name."""
        code = "END: FOR %I FROM 1 TO 10"
        tokens = self.get_tokens(lexer, code)
        # END should be label, not keyword
        assert tokens == [
            (Name.Label, "END"),
            (Punctuation, ":"),
            (Whitespace, " "),
            (Keyword, "FOR"),
            (Whitespace, " "),
            (Name.Variable, "%I"),
            (Whitespace, " "),
            (Keyword, "FROM"),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, " "),
            (Keyword, "TO"),
            (Whitespace, " "),
            (Number.Integer, "10"),
            (Whitespace, "\n"),
        ]


# Integration tests for example files
@pytest.mark.parametrize("example_file", glob("tests/examples/*.soul"))
def test_example_files_produce_no_errors(example_file):
    """Test that example .soul files tokenize without Error tokens."""
    with open(example_file) as f:
        code = f.read()

    lexer = SOULLexer()
    tokens = list(lexer.get_tokens(code))
    error_tokens = [t for t in tokens if t[0] == Error]

    assert len(error_tokens) == 0, f"Error tokens found in {example_file}: {error_tokens}"
