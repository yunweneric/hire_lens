import markdown as md_lib
import nh3

# README-style output only: block scripts, frames, forms, styles and
# anything else that can execute or load active content.
ALLOWED_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "br", "hr",
    "strong", "em", "b", "i", "del", "s",
    "ul", "ol", "li",
    "a", "img",
    "code", "pre", "blockquote",
    "table", "thead", "tbody", "tr", "th", "td",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "img": {"src", "alt", "title"},
    "th": {"align"},
    "td": {"align"},
}

ALLOWED_URL_SCHEMES = {"http", "https", "mailto"}


def render_markdown(text: str) -> str:
    """Render Markdown to sanitized HTML for job descriptions."""
    html = md_lib.markdown(
        text or "",
        extensions=["fenced_code", "tables", "nl2br", "sane_lists"],
    )
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        link_rel="noopener noreferrer",
    )
