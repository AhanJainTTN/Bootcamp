class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_response(self, request, response):
        response["test-header"] = "added by test middleware"
        return response

    def __call__(self, request):
        response = self.get_response(request)
        print(f"Before modification: {response.get("test-header")}")
        response = self.process_response(request, response)
        print(f"After modification:{response.get("test-header")}")
        return response
