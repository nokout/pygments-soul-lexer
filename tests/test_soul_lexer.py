"""
Comprehensive test suite for the SOUL Pygments lexer.
"""

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
        assert tokens[0] == (Comment.Single, "* This is a comment")

    def test_line_comment_with_indent(self, lexer):
        """Test indented line comments."""
        tokens = self.get_tokens(lexer, "    * Indented comment\n")
        assert any(t[0] == Comment.Single for t in tokens)

    def test_block_comment(self, lexer):
        """Test block comments with /? ... ?/."""
        tokens = self.get_tokens(lexer, "/? This is a block comment ?/")
        assert tokens[0] == (Comment.Multiline, "/?")
        assert tokens[-2] == (Comment.Multiline, "?/")

    def test_variable_simple(self, lexer):
        """Test simple percent-prefixed variables."""
        tokens = self.get_tokens(lexer, "%VAR")
        assert (Name.Variable, "%VAR") in tokens

    def test_variable_field(self, lexer):
        """Test field variables with double percent."""
        tokens = self.get_tokens(lexer, "%%FIELD")
        assert (Name.Variable.Global, "%%FIELD") in tokens

    def test_variable_image_item(self, lexer):
        """Test image item references %IMG:ITEM."""
        tokens = self.get_tokens(lexer, "%IMG:FIELD")
        token_types = [t[0] for t in tokens]
        assert Name.Variable in token_types
        assert Name.Attribute in token_types
        assert Punctuation in token_types

    def test_variable_object_method(self, lexer):
        """Test object method calls %OBJ:METHOD(."""
        tokens = self.get_tokens(lexer, "%OBJ:METHOD(")
        token_types = [t[0] for t in tokens]
        assert Name.Variable in token_types
        assert Name.Function in token_types

    def test_dollar_function(self, lexer):
        """Test $Functions (built-in functions)."""
        tokens = self.get_tokens(lexer, "$Len(%STR)")
        assert any(t[0] == Name.Builtin and t[1].startswith("$") for t in tokens)

    def test_string_simple(self, lexer):
        """Test simple string literals."""
        tokens = self.get_tokens(lexer, "'Hello World'")
        assert (String.Single, "'") in tokens
        assert (String.Single, "Hello World") in tokens

    def test_string_escaped_quote(self, lexer):
        """Test strings with escaped quotes ''."""
        tokens = self.get_tokens(lexer, "'It''s working'")
        string_tokens = [t for t in tokens if t[0] == String.Single]
        assert (String.Single, "''") in string_tokens

    @pytest.mark.parametrize("keyword", ["IF", "if", "If", "iF"])
    def test_case_insensitive_keyword(self, lexer, keyword):
        """Test that keywords work regardless of case."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens[0][0] == Keyword

    def test_multi_word_keyword_for_each_record(self, lexer):
        """Test multi-word keyword FOR EACH RECORD."""
        tokens = self.get_tokens(lexer, "FOR EACH RECORD")
        # Should be a single keyword token, not three separate tokens
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 1
        assert "FOR" in keyword_tokens[0][1] and "RECORD" in keyword_tokens[0][1]

    def test_multi_word_keyword_end_if(self, lexer):
        """Test multi-word keyword END IF."""
        tokens = self.get_tokens(lexer, "END IF")
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 1

    def test_label(self, lexer):
        """Test label at start of line."""
        tokens = self.get_tokens(lexer, "LOOP: FOR %I FROM 1 TO 10")
        assert (Name.Label, "LOOP") in tokens
        assert (Punctuation, ":") in tokens

    def test_number_integer(self, lexer):
        """Test integer literals."""
        tokens = self.get_tokens(lexer, "12345")
        assert (Number.Integer, "12345") in tokens

    def test_number_float(self, lexer):
        """Test float literals."""
        tokens = self.get_tokens(lexer, "123.45")
        assert (Number.Float, "123.45") in tokens

    def test_number_scientific(self, lexer):
        """Test scientific notation."""
        tokens = self.get_tokens(lexer, "1.23E+10")
        assert any(t[0] == Number.Float for t in tokens)

    @pytest.mark.parametrize("op", ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>"])
    def test_operator_symbolic(self, lexer, op):
        """Test symbolic operators."""
        tokens = self.get_tokens(lexer, op)
        # Filter out whitespace tokens (trailing newline)
        non_ws_tokens = [t for t in tokens if t[0] != Whitespace]
        assert len(non_ws_tokens) > 0
        assert non_ws_tokens[0][0] == Operator

    @pytest.mark.parametrize("op", ["AND", "OR", "NOT", "EQ", "NE", "GT", "LT"])
    def test_operator_word(self, lexer, op):
        """Test word operators."""
        tokens = self.get_tokens(lexer, op)
        assert tokens[0][0] == Operator.Word

    def test_macro_directive(self, lexer):
        """Test macro directives like !DEF."""
        tokens = self.get_tokens(lexer, "!DEF MACRO_NAME")
        assert any(t[0] == Comment.Preproc for t in tokens)

    def test_text_block_basic(self, lexer):
        """Test TEXT block."""
        code = "TEXT\nHello World\nEND TEXT"
        tokens = self.get_tokens(lexer, code)
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) >= 2  # TEXT and END TEXT

    def test_text_block_interpolation(self, lexer):
        """Test TEXT block with variable interpolation."""
        code = "TEXT\nHello {%NAME}\nEND TEXT"
        tokens = self.get_tokens(lexer, code)
        assert any(t[0] == Name.Variable for t in tokens)

    def test_dummy_string_double_question(self, lexer):
        """Test dummy string ??prompt."""
        tokens = self.get_tokens(lexer, "??ENTER_NAME")
        assert (String.Interpol, "??ENTER_NAME") in tokens

    def test_dummy_string_dollar(self, lexer):
        """Test dummy string ?$prompt."""
        tokens = self.get_tokens(lexer, "?$ENTER_VALUE")
        assert (String.Interpol, "?$ENTER_VALUE") in tokens

    def test_dummy_string_ampersand(self, lexer):
        """Test dummy string ?&global."""
        tokens = self.get_tokens(lexer, "?&GLOBAL_VAR")
        assert (String.Interpol, "?&GLOBAL_VAR") in tokens

    def test_dummy_string_exclamation(self, lexer):
        """Test dummy string ?!macro."""
        tokens = self.get_tokens(lexer, "?!MACRO_VAR")
        assert (String.Interpol, "?!MACRO_VAR") in tokens

    def test_line_continuation(self, lexer):
        """Test line continuation with trailing hyphen."""
        tokens = self.get_tokens(lexer, "PRINT %VAR -\n + 1")
        # Line continuation should be treated as whitespace
        assert any(t[0] == Whitespace and "-" in t[1] for t in tokens)

    @pytest.mark.parametrize("keyword", ["DECLARE", "IMAGE", "CLASS", "FUNCTION", "PROCEDURE"])
    def test_declaration_keyword(self, lexer, keyword):
        """Test declaration keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens[0][0] == Keyword.Declaration

    @pytest.mark.parametrize("keyword", ["FIXED", "FLOAT", "STRING", "ARRAY"])
    def test_type_keyword(self, lexer, keyword):
        """Test type keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens[0][0] == Keyword.Type

    @pytest.mark.parametrize("keyword", ["PUBLIC", "PRIVATE", "SHARED", "STATIC"])
    def test_visibility_keyword(self, lexer, keyword):
        """Test visibility keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens[0][0] == Keyword.Declaration

    @pytest.mark.parametrize("keyword", ["FIND", "STORE", "UPDATE", "DELETE", "FDR", "FRN"])
    def test_database_keyword(self, lexer, keyword):
        """Test database operation keywords."""
        tokens = self.get_tokens(lexer, keyword)
        assert tokens[0][0] == Keyword

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
        assert tokens[0][0] == Keyword

    def test_complex_expression(self, lexer):
        """Test a complex expression with multiple token types."""
        code = "%RESULT = $Len(%NAME) + 10"
        tokens = self.get_tokens(lexer, code)

        token_types = [t[0] for t in tokens]
        assert Name.Variable in token_types  # %RESULT and %NAME
        assert Name.Builtin in token_types  # $Len
        assert Operator in token_types  # = and +
        assert Number.Integer in token_types  # 10

    def test_find_all_records_statement(self, lexer):
        """Test FIND ALL RECORDS as a single multi-word keyword."""
        tokens = self.get_tokens(lexer, "FIND ALL RECORDS IN FILE")
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        # FIND ALL RECORDS should be one token, IN should be another
        assert len(keyword_tokens) >= 2

    def test_store_record_statement(self, lexer):
        """Test STORE RECORD as a single multi-word keyword."""
        tokens = self.get_tokens(lexer, "STORE RECORD")
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 1

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
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 2  # TEXT and END TEXT

    def test_keyword_prefix_not_matched(self, lexer):
        """Test that FIND1 is not matched as FIND keyword."""
        tokens = self.get_tokens(lexer, "FIND1")
        # Should be Name, not Keyword (word boundary check)
        assert tokens[0][0] == Name

    def test_end_text_outside_block(self, lexer):
        """Test END TEXT outside a TEXT block is handled."""
        tokens = self.get_tokens(lexer, "END TEXT")
        # Should be recognized as a keyword even in root state
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 1

    def test_nested_interpolation(self, lexer):
        """Test nested braces in TEXT block interpolation."""
        code = "TEXT\n{%VAR}\nEND TEXT"
        tokens = list(self.get_tokens(lexer, code))
        # Should have interpolation punctuation
        assert (Punctuation, "{") in tokens
        assert (Punctuation, "}") in tokens
        assert any(t[0] == Name.Variable for t in tokens)

    def test_windows_line_endings(self, lexer):
        """Test Windows \\r\\n line endings work correctly."""
        code = "* Comment\r\n%VAR = 1\r\n"
        tokens = list(self.get_tokens(lexer, code))
        assert any(t[0] == Comment.Single for t in tokens)
        assert any(t[0] == Name.Variable for t in tokens)

    def test_empty_comment(self, lexer):
        """Test comment with only asterisk and space."""
        tokens = self.get_tokens(lexer, "* ")
        assert tokens[0][0] == Comment.Single

    def test_comment_after_blank_lines(self, lexer):
        """Test comment recognition after multiple blank lines."""
        code = "\n\n    * This is a comment"
        tokens = self.get_tokens(lexer, code)
        comment_tokens = [t for t in tokens if t[0] == Comment.Single]
        assert len(comment_tokens) == 1

    def test_multi_word_keyword_extra_spaces(self, lexer):
        """Test multi-word keyword with extra spaces."""
        tokens = self.get_tokens(lexer, "FOR  EACH  RECORD")
        # Should still match as keyword (uses [ \\t]+ pattern)
        keyword_tokens = [t for t in tokens if t[0] == Keyword]
        assert len(keyword_tokens) == 1

    def test_label_keyword_name(self, lexer):
        """Test label that matches keyword name."""
        code = "END: FOR %I FROM 1 TO 10"
        tokens = self.get_tokens(lexer, code)
        # END should be label, not keyword
        assert (Name.Label, "END") in tokens
        assert (Punctuation, ":") in tokens
