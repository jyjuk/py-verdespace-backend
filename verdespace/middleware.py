class RemoveAuthorizationHeaderMiddleware:
    """
    Middleware для видалення заголовка Authorization із запитів до S3.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "s3.amazonaws.com" in request.build_absolute_uri():
            if "HTTP_AUTHORIZATION" in request.META:
                del request.META["HTTP_AUTHORIZATION"]
        return self.get_response(request)
