import logging

logger = logging.getLogger("request_metadata")


class RequestMetadataMiddleware:
    """Middleware to log request metadata."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):
        logger.info(request.META)
        return self.get_response(request)
