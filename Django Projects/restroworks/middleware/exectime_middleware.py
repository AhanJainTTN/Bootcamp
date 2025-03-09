import time


class ExecTimeMiddleware:
    """Middleware to track request execution time."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        print(f"Request took {(end_time - start_time):.2f} seconds")
        return response
