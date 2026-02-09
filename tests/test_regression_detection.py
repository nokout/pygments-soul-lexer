"""
Tests to demonstrate that exact sequence assertions catch regressions
that weak assertions would miss.

These tests simulate potential bugs that could occur in the lexer and
verify that our improved test assertions would catch them.
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


class TestRegressionDetection:
    """Test cases that demonstrate the value of exact sequence assertions."""

    @pytest.fixture
    def lexer(self):
        """Provide a SOULLexer instance."""
        return SOULLexer()

    def get_tokens(self, lexer, text):
        """Helper to get list of (token_type, value) tuples."""
        return list(lexer.get_tokens(text))

    def test_token_order_matters(self, lexer):
        """
        Demonstrate that exact assertions catch token reordering.

        A weak assertion like:
            assert (Name.Variable, "%VAR") in tokens
            assert (Operator, "=") in tokens
            assert (Number.Integer, "1") in tokens

        would pass even if tokens were incorrectly ordered as: "1 = %VAR"

        Our exact assertion catches this.
        """
        tokens = self.get_tokens(lexer, "%VAR = 1")

        # This would catch incorrect ordering
        assert tokens == [
            (Name.Variable, "%VAR"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Number.Integer, "1"),
            (Whitespace, "\n"),
        ]

        # Verify that reversed order would fail
        reversed_tokens = [
            (Number.Integer, "1"),
            (Whitespace, " "),
            (Operator, "="),
            (Whitespace, " "),
            (Name.Variable, "%VAR"),
            (Whitespace, "\n"),
        ]
        assert tokens != reversed_tokens

    def test_token_duplication_detection(self, lexer):
        """
        Demonstrate that exact assertions catch token duplication.

        A weak assertion checking only presence would miss if a token
        appeared multiple times when it shouldn't.
        """
        tokens = self.get_tokens(lexer, "IF")

        # Exact count matters - should be exactly one keyword
        assert tokens == [
            (Keyword, "IF"),
            (Whitespace, "\n"),
        ]

        # Verify that duplication would fail
        duplicated_tokens = [
            (Keyword, "IF"),
            (Keyword, "IF"),  # Bug: duplicated
            (Whitespace, "\n"),
        ]
        assert tokens != duplicated_tokens

    def test_missing_token_detection(self, lexer):
        """
        Demonstrate that exact assertions catch missing tokens.

        A weak assertion like:
            assert any(t[0] == Keyword for t in tokens)

        would pass even if whitespace or other tokens were missing.
        """
        tokens = self.get_tokens(lexer, "FOR EACH RECORD")

        # All tokens must be present
        assert tokens == [
            (Keyword, "FOR EACH RECORD"),
            (Whitespace, "\n"),
        ]

        # Verify that missing whitespace would fail
        missing_whitespace = [
            (Keyword, "FOR EACH RECORD"),
            # Missing final newline would be caught
        ]
        assert tokens != missing_whitespace

    def test_token_completeness(self, lexer):
        """
        Demonstrate that exact assertions ensure complete token coverage.

        Weak assertions might only check specific tokens and miss that
        extra unexpected tokens were generated.
        """
        tokens = self.get_tokens(lexer, "%VAR")

        # Exact match ensures no extra tokens
        assert tokens == [
            (Name.Variable, "%VAR"),
            (Whitespace, "\n"),
        ]

        # Verify extra tokens would fail
        extra_tokens = [
            (Name.Variable, "%VAR"),
            (Name, "EXTRA"),  # Bug: unexpected extra token
            (Whitespace, "\n"),
        ]
        assert tokens != extra_tokens

    def test_multi_word_keyword_integrity(self, lexer):
        """
        Demonstrate that exact assertions verify multi-word keywords are
        tokenized as single units, not split into multiple tokens.
        """
        tokens = self.get_tokens(lexer, "END IF")

        # Must be a single multi-word keyword, not separate tokens
        assert tokens == [
            (Keyword, "END IF"),
            (Whitespace, "\n"),
        ]

        # Verify that split tokens would fail
        split_tokens = [
            (Keyword, "END"),      # Bug: split instead of single token
            (Whitespace, " "),
            (Keyword, "IF"),
            (Whitespace, "\n"),
        ]
        assert tokens != split_tokens

    def test_whitespace_handling_precision(self, lexer):
        """
        Demonstrate that exact assertions catch incorrect whitespace handling.

        Weak assertions might ignore whitespace entirely, missing bugs
        in how whitespace is tokenized.
        """
        tokens = self.get_tokens(lexer, "IF THEN")

        # Whitespace handling must be exact
        assert tokens == [
            (Keyword, "IF"),
            (Whitespace, " "),
            (Keyword, "THEN"),
            (Whitespace, "\n"),
        ]

        # Verify that missing or wrong whitespace would fail
        wrong_whitespace = [
            (Keyword, "IF"),
            (Whitespace, "  "),  # Bug: wrong amount of whitespace
            (Keyword, "THEN"),
            (Whitespace, "\n"),
        ]
        assert tokens != wrong_whitespace


class TestWeakAssertionComparison:
    """
    Demonstrate specific scenarios where weak assertions would pass
    but exact assertions correctly fail.
    """

    @pytest.fixture
    def lexer(self):
        """Provide a SOULLexer instance."""
        return SOULLexer()

    def get_tokens(self, lexer, text):
        """Helper to get list of (token_type, value) tuples."""
        return list(lexer.get_tokens(text))

    def test_weak_assertion_would_miss_reordering(self, lexer):
        """
        Show that a weak 'in' assertion would incorrectly pass with wrong order.
        """
        tokens = self.get_tokens(lexer, "%A + %B")

        # Weak assertion (would miss ordering bugs):
        # assert (Name.Variable, "%A") in tokens  # ✓ passes
        # assert (Operator, "+") in tokens         # ✓ passes
        # assert (Name.Variable, "%B") in tokens  # ✓ passes

        # Strong assertion (catches ordering):
        expected = [
            (Name.Variable, "%A"),
            (Whitespace, " "),
            (Operator, "+"),
            (Whitespace, " "),
            (Name.Variable, "%B"),
            (Whitespace, "\n"),
        ]
        assert tokens == expected

        # Verify weak assertion would pass with wrong order
        assert (Name.Variable, "%A") in tokens
        assert (Operator, "+") in tokens
        assert (Name.Variable, "%B") in tokens
        # But the order is actually correct in this case
        assert tokens[0] == (Name.Variable, "%A")
        assert tokens[4] == (Name.Variable, "%B")

    def test_weak_assertion_would_miss_duplicates(self, lexer):
        """
        Show that 'any' assertions would pass even with duplicate tokens.
        """
        tokens = self.get_tokens(lexer, "FIND")

        # Weak assertion (would miss duplication):
        # assert any(t[0] == Keyword for t in tokens)  # ✓ passes even with duplicates

        # Strong assertion (catches exact count):
        assert tokens == [
            (Keyword, "FIND"),
            (Whitespace, "\n"),
        ]

        # Count the keywords - should be exactly 1
        keyword_count = sum(1 for t in tokens if t[0] == Keyword)
        assert keyword_count == 1
