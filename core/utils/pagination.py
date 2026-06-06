from django.core.paginator import Page, Paginator

DEFAULT_PER_PAGE = 5


def paginate(request, object_list, per_page: int = DEFAULT_PER_PAGE) -> Page:
    """Return the requested page of ``object_list``.

    Reads the page number from ``?page=`` and falls back gracefully to the
    first/last valid page for missing or out-of-range values.
    """
    paginator = Paginator(object_list, per_page)
    return paginator.get_page(request.GET.get("page"))
