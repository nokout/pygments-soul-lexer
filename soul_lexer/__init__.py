"""
Pygments lexer for SOUL (System Online User Language).

SOUL is the 4GL programming language for Rocket Software's Model 204 database system.
"""

from importlib.metadata import version, PackageNotFoundError
from soul_lexer.lexer import SOULLexer

try:
    __version__ = version("pygments-soul-lexer")
except PackageNotFoundError:
    # Package is not installed, probably running from source
    __version__ = "unknown"

__all__ = ["SOULLexer"]
