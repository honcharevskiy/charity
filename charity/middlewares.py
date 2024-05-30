from django.http import HttpRequest

from charity import settings


class LanguageMiddleware:
    """Determine language based on query parameters."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.language = request.GET.get('lan', settings.DEFAULT_LANGUAGE).lower()
        response = self.get_response(request)
        return response
