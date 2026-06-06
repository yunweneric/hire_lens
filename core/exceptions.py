"""Shared exceptions for HireLens."""


class HireLensError(Exception):
    """Base exception for HireLens."""


class ResumeParseError(HireLensError):
    """Raised when resume text extraction fails."""


class GeminiAPIError(HireLensError):
    """Raised when Gemini API call fails."""
