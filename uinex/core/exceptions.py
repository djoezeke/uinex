"""Uinex Exceptions

Custom exception classes for the Uinex UI library.

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

__all__ = ["UinexError", "ThemeError", "WidgetError", "GeometryError"]


class UinexError(Exception):
    """Base exception for all Uinex errors."""


class ThemeError(UinexError):
    """Raised when a theme operation fails (e.g., invalid theme name or file)."""


class WidgetError(UinexError):
    """Raised when a widget operation fails."""


class GeometryError(UinexError):
    """Raised when a geometry management operation fails."""
