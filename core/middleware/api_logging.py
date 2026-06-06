"""API request logging middleware stub. Full implementation in Phase 2."""


class APILoggingMiddleware:
    """Log API requests to APIUsageLog. Stub for scaffold."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
