# Data Flow

## Public application flow

```mermaid
sequenceDiagram
    participant C as Candidate
    participant P as PublicSite
    participant D as Django
    participant M as MediaStore

    C->>P: Browse /jobs/
    C->>P: Open job detail
    C->>P: Submit apply form + resume
    P->>D: POST /jobs/slug/apply/
    D->>D: Parse PDF/DOCX
    D->>M: Store resume file
    D->>D: Create Resume + Application
    P->>C: Success page
```

## Admin AI analysis flow

```mermaid
sequenceDiagram
    participant A as Admin
    participant D as Django
    participant G as GeminiAPI

    A->>D: POST analyze application
    D->>G: resume text + job Markdown
    G->>D: JSON match result
    D->>D: Save/update Analysis
    A->>D: View rankings per job
```

## Routes

| Surface | Path | Auth |
|---------|------|------|
| Public jobs | `/jobs/` | None |
| Apply | `/jobs/<slug>/apply/` | None |
| Admin | `/admin/` | Login + admin role |
| Login | `/accounts/login/` | None |
