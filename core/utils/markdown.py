import markdown as md_lib


def render_markdown(text: str) -> str:
    """Render Markdown to safe HTML for job descriptions."""
    return md_lib.markdown(
        text or "",
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    )
