# Feature: Resumes

**Package:** `features.resumes`

## Responsibility

Resume file upload, text extraction, and listing.

## Models

- `Resume` — File, raw text, candidate name, uploader

## Views

| URL | View | Auth |
|-----|------|------|
| `/resumes/` | Resume list | Required |
| `/resumes/upload/` | Upload form | Required |

## Services

- `upload_resume(file, user, candidate_name)` — Validates, parses, saves
- `list_resumes(user)` — Returns queryset for user (all for admin)

## Dependencies

- `core.parsers.resume.ResumeParser` — PDF/DOCX text extraction

## API

- `POST /api/resumes/upload/` — Multipart file upload

## Supported Formats

- PDF (via pdfplumber)
- DOCX (via python-docx)

## Validation

- Max file size: 5 MB
- Allowed extensions: `.pdf`, `.docx`
