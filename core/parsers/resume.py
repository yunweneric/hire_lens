"""Resume text extraction from PDF and DOCX files."""
import io
from pathlib import Path

import pdfplumber
from docx import Document

from core.exceptions import ResumeParseError


class ResumeParser:
    """Extract plain text from resume files."""

    SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

    def extract_text(self, file) -> str:
        """
        Extract text from an uploaded file.

        Args:
            file: Django UploadedFile or file-like object with a name attribute.

        Returns:
            Extracted plain text string.

        Raises:
            ResumeParseError: If format is unsupported or extraction fails.
        """
        filename = getattr(file, "name", "upload")
        ext = Path(filename).suffix.lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ResumeParseError(f"Unsupported file format: {ext}")

        if ext == ".pdf":
            return self._extract_pdf(file)
        return self._extract_docx(file)

    def _extract_pdf(self, file) -> str:
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
            text = "\n".join(pages).strip()
            if not text:
                raise ResumeParseError("Could not extract text from PDF.")
            return text
        except ResumeParseError:
            raise
        except Exception as exc:
            raise ResumeParseError(f"PDF parsing failed: {exc}") from exc

    def _extract_docx(self, file) -> str:
        try:
            file.seek(0)
            content = file.read() if hasattr(file, "read") else file
            doc = Document(io.BytesIO(content))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            text = "\n".join(paragraphs).strip()
            if not text:
                raise ResumeParseError("Could not extract text from DOCX.")
            return text
        except ResumeParseError:
            raise
        except Exception as exc:
            raise ResumeParseError(f"DOCX parsing failed: {exc}") from exc
