"""
Tests for exact token sequence validation feature.

This test suite validates that the lexer produces exact, correct token
sequences. It ensures that token ordering, completeness, and precision
are properly maintained, which is critical for accurate syntax highlighting.

These tests verify the token sequence validation feature works correctly
by checking:
- Token ordering is preserved
- No token duplication occurs
- All expected tokens are present
- No unexpected extra tokens appear
- Multi-word keywords remain intact
- Whitespace is handled precisely
"""

import pytest
from pygments.token import (
    Keyword,
    Name,
    Number,
    Operator,
    Whitespace,
)

from soul_lexer.lexer import SOULLexer


class TestExactTokenSequenceMatching:
    """Test exact token sequence matching validates lexer output correctly."""

    @pytest.fixture
    def lexer(self):
        """Provide a SOULLexer instance."""
        return SOULLexer()

    def get_tokens(self, lexer, text):
        """Helper to get list of (token_type, value) tuples."""
        return list(lexer.get_tokens(text))

    def test_exact_sequence_validates_token_order(self, lexer):
        """
        Test that exact sequence matching validates correct token ordering.

        Verifies that the token sequence validation feature correctly
        identifies when tokens are in the expected order, and would detect
        if they were incorrectly reordered.
        """
        tokens = self.get_tokens(lexer, "%VAR = 1")

        # Validate correct token sequence
        assert tokens == [
            (Name.Variable, "%VAR"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, "\n"),
        ]

        # Verify that reversed order would be detected as incorrect
        reversed_tokens = [
            (Number.Integer, "1"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Name.Variable, "%VAR"),
            (Whitespace, "\n"),
        ]
        assert tokens != reversed_tokens

    def test_exact_sequence_detects_duplicates(self, lexer):
        """
        Test that exact sequence matching detects duplicate tokens.

        Verifies that the token sequence validation feature ensures
        tokens are not duplicated when they should appear only once.
        """
        tokens = self.get_tokens(lexer, "IF")

        # Validate correct single keyword
        assert tokens == [
            (Keyword, "IF"),
            (Whitespace, "\n"),
        ]

        # Verify that duplication would be detected
        duplicated_tokens = [
            (Keyword, "IF"),
            (Keyword, "IF"),  # Duplicate would be caught
            (Whitespace, "\n"),
        ]
        assert tokens != duplicated_tokens

    def test_exact_sequence_detects_missing_tokens(self, lexer):
        """
        Test that exact sequence matching detects missing tokens.

        Verifies that the token sequence validation feature ensures
        all expected tokens are present in the output.
        """
        tokens = self.get_tokens(lexer, "FOR EACH RECORD")

        # Validate all tokens are present
        assert tokens == [
            (Keyword, "FOR EACH RECORD"),
            (Whitespace, "\n"),
        ]

        # Verify that missing tokens would be detected
        missing_whitespace = [
            (Keyword, "FOR EACH RECORD"),
            # Missing final newline would be caught
        ]
        assert tokens != missing_whitespace

    def test_exact_sequence_ensures_completeness(self, lexer):
        """
        Test that exact sequence matching ensures complete token coverage.

        Verifies that the token sequence validation feature detects when
        unexpected extra tokens appear in the output.
        """
        tokens = self.get_tokens(lexer, "%VAR")

        # Validate exact token sequence with no extras
        assert tokens == [
            (Name.Variable, "%VAR"),
            (Whitespace, "\n"),
        ]

        # Verify extra tokens would be detected
        extra_tokens = [
            (Name.Variable, "%VAR"),
            (Name, "EXTRA"),  # Extra token would be caught
            (Whitespace, "\n"),
        ]
        assert tokens != extra_tokens

    def test_exact_sequence_validates_multi_word_keywords(self, lexer):
        """
        Test that exact sequence matching validates multi-word keyword integrity.

        Verifies that the token sequence validation feature ensures
        multi-word keywords are tokenized as single units rather than
        being incorrectly split into multiple tokens.
        """
        tokens = self.get_tokens(lexer, "END IF")

        # Validate multi-word keyword is a single token
        assert tokens == [
            (Keyword, "END IF"),
            (Whitespace, "\n"),
        ]

        # Verify that split tokens would be detected
        split_tokens = [
            (Keyword, "END"),  # Incorrectly split
            (Whitespace, " "),
            (Keyword, "IF"),
            (Whitespace, "\n"),
        ]
        assert tokens != split_tokens

    def test_exact_sequence_validates_whitespace(self, lexer):
        """
        Test that exact sequence matching validates whitespace handling.

        Verifies that the token sequence validation feature ensures
        whitespace is tokenized with correct precision and amount.
        """
        tokens = self.get_tokens(lexer, "IF THEN")

        # Validate exact whitespace handling
        assert tokens == [
            (Keyword, "IF"),
            (Whitespace, " "),
            (Keyword, "THEN"),
            (Whitespace, "\n"),
        ]

        # Verify that incorrect whitespace would be detected
        wrong_whitespace = [
            (Keyword, "IF"),
            (Whitespace, "  "),  # Wrong amount would be caught
            (Keyword, "THEN"),
            (Whitespace, "\n"),
        ]
        assert tokens != wrong_whitespace


class TestTokenSequenceOrdering:
    """
    Test token sequence ordering validation for complex expressions.

    Validates that token ordering is properly maintained in expressions
    with multiple tokens of different types.
    """

    @pytest.fixture
    def lexer(self):
        """Provide a SOULLexer instance."""
        return SOULLexer()

    def get_tokens(self, lexer, text):
        """Helper to get list of (token_type, value) tuples."""
        return list(lexer.get_tokens(text))

    def test_token_ordering_validation(self, lexer):
        """
        Test that token sequence validation maintains correct order in expressions.

        Validates that tokens appear in the correct sequence for expressions
        with multiple variables and operators.
        """
        tokens = self.get_tokens(lexer, "%A + %B")

        # Validate correct token ordering
        expected = [
            (Name.Variable, "%A"),
            (Whitespace, " "),
            (Operator, "+"),
            (Whitespace, " "),
            (Name.Variable, "%B"),
            (Whitespace, "\n"),
        ]
        assert tokens == expected

        # Verify tokens are in correct positions
        assert tokens[0] == (Name.Variable, "%A")
        assert tokens[2] == (Operator, "+")
        assert tokens[4] == (Name.Variable, "%B")

    def test_token_duplication_validation(self, lexer):
        """
        Test that token sequence validation detects duplicate keywords.

        Validates that keywords appear exactly once when expected,
        not duplicated.
        """
        tokens = self.get_tokens(lexer, "FIND")

        # Validate exact token count and sequence
        assert tokens == [
            (Keyword, "FIND"),
            (Whitespace, "\n"),
        ]

        # Verify keyword appears exactly once
        keyword_count = sum(1 for t in tokens if t[0] == Keyword)
        assert keyword_count == 1
