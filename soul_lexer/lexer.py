"""
Pygments lexer for SOUL (System Online User Language).

SOUL is the 4GL programming language for Rocket Software's Model 204 database system.
It features percent-prefixed variables, dollar-prefixed built-in functions, database
operations, object-oriented programming, and text interpolation blocks.
"""

import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)

__all__ = ["SOULLexer"]


class SOULLexer(RegexLexer):
    """
    Lexer for SOUL (System Online User Language), the 4GL language for Model 204.

    .. versionadded:: 0.1.0
    """

    name = "SOUL"
    aliases = ["soul", "model204"]
    filenames = ["*.soul", "*.m204", "*.proc"]
    mimetypes = ["text/x-soul"]
    url = "https://m204wiki.rocketsoftware.com/"

    flags = re.IGNORECASE | re.MULTILINE

    def analyse_text(text):
        """Return confidence that this text is SOUL code."""
        result = 0.0
        # Strong indicators
        if re.search(r'^\s*\*', text, re.MULTILINE):
            result += 0.1  # Line comments
        if re.search(r'%\w+', text):
            result += 0.2  # Percent variables
        if re.search(r'\$\w+', text):
            result += 0.1  # Dollar functions
        if re.search(r'\bFOR\s+EACH\s+RECORD\b', text, re.IGNORECASE):
            result += 0.4  # Very SOUL-specific
        if re.search(r'/\?.*\?/', text, re.DOTALL):
            result += 0.2  # Block comments
        return min(result, 1.0)

    tokens = {
        "root": [
            # Comments - line comments must be first non-blank on line
            # Check both at start and after newlines (handles multiple blank lines too)
            (r"^([ \t]*)(\*.+)$", bygroups(Whitespace, Comment.Single)),
            (r"(\n+)([ \t]*)(\*.+)$", bygroups(Whitespace, Whitespace, Comment.Single)),

            # Whitespace and line continuation
            # Line continuation must not be at the very start
            (r"(?<!^)-\s*\n", Whitespace),  # Line continuation
            # Don't consume newlines if followed by optional spaces/tabs and asterisk (comment)
            (r"[ \t]+", Whitespace),  # Non-newline whitespace
            (r"\n(?![ \t]*\*)", Whitespace),  # Newline not followed by comment

            # Block comments
            (r"/\?", Comment.Multiline, "block-comment"),

            # Macro directives
            (
                r"^(\s*)(!)(DEF|UNDEF|IFDEF|IFNDEF|ELSE|ENDIF|IF|THEN)\b",
                bygroups(Whitespace, Comment.Preproc, Comment.Preproc),
            ),

            # Labels (must be at start of line)
            (
                r"^(\s*)([a-z_]\w*)(:)(\s)",
                bygroups(Whitespace, Name.Label, Punctuation, Whitespace),
            ),

            # TEXT and HTML blocks
            (r"\b(TEXT)\b", Keyword, "text-block"),
            (r"\b(HTML)\b", Keyword, "html-block"),

            # Strings
            (r"'", String.Single, "string"),

            # Dummy strings - ordered by specificity
            (r"\?\?[^\s]+", String.Interpol),  # ??prompt
            (r"\?\$[^\s]+", String.Interpol),  # ?$prompt
            (r"\?&[a-z_]\w*", String.Interpol),  # ?&global
            (r"\?![a-z_]\w*", String.Interpol),  # ?!macro_var

            # Numbers
            (r"[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?", Number.Float),  # Float
            (r"[0-9]+[eE][+-]?[0-9]+", Number.Float),  # Scientific notation
            (r"[0-9]+", Number.Integer),  # Integer

            # $Functions (built-in functions)
            (r"\$[a-z_]\w*", Name.Builtin),

            # Variables - most specific first
            # Object method calls: %OBJ:METHOD(
            (
                r"(%[a-z_]\w*)(:)([a-z_]\w*)(\()",
                bygroups(Name.Variable, Punctuation, Name.Function, Punctuation),
            ),
            # Image items: %IMG:ITEM
            (
                r"(%[a-z_]\w*)(:)([a-z_]\w*)",
                bygroups(Name.Variable, Punctuation, Name.Attribute),
            ),
            # Field variables (double percent)
            (r"%%[a-z_]\w*", Name.Variable.Global),
            # Regular variables
            (r"%[a-z_]\w*", Name.Variable),

            # Multi-word keywords - longest first to avoid partial matches
            (r"\b(FOR[ \t]+EACH[ \t]+RECORD)\b", Keyword),
            (r"\b(FOR[ \t]+EACH[ \t]+VALUE)\b", Keyword),
            (r"\b(FOR[ \t]+EACH[ \t]+OCCURRENCE)\b", Keyword),
            (r"\b(FIND[ \t]+ALL[ \t]+RECORDS)\b", Keyword),
            (r"\b(FIND[ \t]+ALL[ \t]+VALUES)\b", Keyword),
            (r"\b(STORE[ \t]+RECORD)\b", Keyword),
            (r"\b(UPDATE[ \t]+RECORD)\b", Keyword),
            (r"\b(DELETE[ \t]+RECORD)\b", Keyword),

            # END statements
            (r"\b(END[ \t]+IF)\b", Keyword),
            (r"\b(END[ \t]+FOR)\b", Keyword),
            (r"\b(END[ \t]+REPEAT)\b", Keyword),
            (r"\b(END[ \t]+CLASS)\b", Keyword),
            (r"\b(END[ \t]+IMAGE)\b", Keyword),
            (r"\b(END[ \t]+PROCEDURE)\b", Keyword),
            (r"\b(END[ \t]+FUNCTION)\b", Keyword),
            (r"\b(END[ \t]+SUBROUTINE)\b", Keyword),
            (r"\b(END[ \t]+TEXT)\b", Keyword),
            (r"\b(END[ \t]+HTML)\b", Keyword),
            (r"\b(END[ \t]+TRY)\b", Keyword),
            (r"\b(END[ \t]+CATCH)\b", Keyword),
            (r"\b(END[ \t]+BLOCK)\b", Keyword),

            # Other multi-word constructs
            (r"\b(VARIABLES[ \t]+ARE)\b", Keyword.Declaration),
            (r"\b(REPEAT[ \t]+WHILE)\b", Keyword),
            (r"\b(REPEAT[ \t]+UNTIL)\b", Keyword),

            # Word operators with multi-word forms
            (r"\b(IS[ \t]+NOT[ \t]+LIKE)\b", Operator.Word),
            (r"\b(IS[ \t]+LIKE)\b", Operator.Word),
            (r"\b(IS[ \t]+NOT[ \t]+PRESENT)\b", Operator.Word),
            (r"\b(IS[ \t]+PRESENT)\b", Operator.Word),

            # Declaration keywords
            (
                words(
                    (
                        "DECLARE",
                        "IMAGE",
                        "CLASS",
                        "ENUMERATION",
                        "PROCEDURE",
                        "FUNCTION",
                        "SUBROUTINE",
                        "PROPERTY",
                        "CONSTRUCTOR",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword.Declaration,
            ),

            # Type keywords
            (
                words(
                    (
                        "FIXED",
                        "FLOAT",
                        "STRING",
                        "LEN",
                        "DP",
                        "ARRAY",
                        "INITIAL",
                        "UNDEFINED",
                        "OBJECT",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword.Type,
            ),

            # Visibility/scope keywords
            (
                words(
                    ("PUBLIC", "PRIVATE", "SHARED", "STATIC"),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword.Declaration,
            ),

            # Control flow keywords
            (
                words(
                    (
                        "IF",
                        "THEN",
                        "ELSE",
                        "ELSEIF",
                        "FOR",
                        "TO",
                        "FROM",
                        "BY",
                        "REPEAT",
                        "WHILE",
                        "UNTIL",
                        "BEGIN",
                        "END",
                        "CALL",
                        "RETURN",
                        "TRY",
                        "CATCH",
                        "THROW",
                        "JUMP",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword,
            ),

            # Database operation keywords (including abbreviations)
            (
                words(
                    (
                        "FIND",
                        "STORE",
                        "UPDATE",
                        "DELETE",
                        "FD",
                        "FDR",
                        "FDV",
                        "FR",
                        "FRN",
                        "FRV",
                        "FEO",
                        "FPC",
                        "AAI",
                        "CH",
                        "CT",
                        "ST",
                        "PAI",
                        "NP",
                        "ADD",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword,
            ),

            # Other common keywords
            (
                words(
                    (
                        "IN",
                        "PRINT",
                        "AUDIT",
                        "SKIP",
                        "LINES",
                        "NEW",
                        "IS",
                        "RECORDS",
                        "VALUE",
                        "OCCURRENCE",
                        "ALL",
                        "WHERE",
                        "AT",
                        "ON",
                        "COUNT",
                        "SORT",
                        "COUNTED",
                        "ORDERED",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Keyword,
            ),

            # Word operators
            (
                words(
                    (
                        "AND",
                        "OR",
                        "NOT",
                        "NOR",
                        "ANDIF",
                        "ORIF",
                        "EQ",
                        "NE",
                        "GT",
                        "LT",
                        "GE",
                        "LE",
                        "WITH",
                        "LIKE",
                        "PRESENT",
                    ),
                    prefix=r"\b",
                    suffix=r"\b",
                ),
                Operator.Word,
            ),

            # Symbolic operators
            (r"<>", Operator),
            (r">=", Operator),
            (r"<=", Operator),
            (r"[+\-*/=<>]", Operator),

            # Punctuation
            (r"[(),:.\[\]]", Punctuation),

            # Identifiers (catch-all)
            (r"[a-z_]\w*", Name),
        ],
        "block-comment": [
            (r"\?/", Comment.Multiline, "#pop"),
            (r"[^?]+", Comment.Multiline),
            (r"\?", Comment.Multiline),
        ],
        "string": [
            (r"''", String.Single),  # Escaped quote
            (r"'", String.Single, "#pop"),  # End of string
            (r"[^']+", String.Single),  # String content
        ],
        "text-block": [
            (r"END[ \t]+TEXT\b", Keyword, "#pop"),
            (r"\{", Punctuation, "interpolation"),
            (r"[^\{]+?(?=END[ \t]+TEXT|\{)", String),
            (r"[^\{]+", String),  # Fallback for end of input
        ],
        "html-block": [
            (r"END[ \t]+HTML\b", Keyword, "#pop"),
            (r"\{", Punctuation, "interpolation"),
            (r"[^\{]+?(?=END[ \t]+HTML|\{)", String),
            (r"[^\{]+", String),  # Fallback for end of input
        ],
        "interpolation": [
            (r"\}", Punctuation, "#pop"),

            # Include most root patterns for expressions inside braces
            (r"\s+", Whitespace),
            (r"'", String.Single, "string"),

            # Numbers
            (r"[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?", Number.Float),
            (r"[0-9]+[eE][+-]?[0-9]+", Number.Float),
            (r"[0-9]+", Number.Integer),

            # $Functions
            (r"\$[a-z_]\w*", Name.Builtin),

            # Variables
            (
                r"(%[a-z_]\w*)(:)([a-z_]\w*)(\()",
                bygroups(Name.Variable, Punctuation, Name.Function, Punctuation),
            ),
            (
                r"(%[a-z_]\w*)(:)([a-z_]\w*)",
                bygroups(Name.Variable, Punctuation, Name.Attribute),
            ),
            (r"%%[a-z_]\w*", Name.Variable.Global),
            (r"%[a-z_]\w*", Name.Variable),

            # Operators
            (r"<>", Operator),
            (r">=", Operator),
            (r"<=", Operator),
            (r"[+\-*/=<>]", Operator),

            # Punctuation
            (r"[(),:.\[\]]", Punctuation),

            # Identifiers
            (r"[a-z_]\w*", Name),
        ],
    }
