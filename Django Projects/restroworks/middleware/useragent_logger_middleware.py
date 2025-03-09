class UserAgentLoggerMiddleware:
    """Middleware to log user agent."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):
        user_agent = request.META.get("HTTP_USER_AGENT")
        print(user_agent)
        response = self.get_response(request)
        return response


request_dict = {
    "SERVER_PORT": "8000",
    "REMOTE_HOST": "",
    "CONTENT_LENGTH": "",
    "SCRIPT_NAME": "",
    "SERVER_PROTOCOL": "HTTP/1.1",
    "SERVER_SOFTWARE": "WSGIServer/0.2",
    "REQUEST_METHOD": "GET",
    "PATH_INFO": "/admin/customers/customer/",
    "QUERY_STRING": "",
    "REMOTE_ADDR": "127.0.0.1",
    "CONTENT_TYPE": "text/plain",
    "HTTP_HOST": "127.0.0.1:8000",
    "HTTP_CONNECTION": "keep-alive",
    "HTTP_SEC_CH_UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "HTTP_SEC_CH_UA_MOBILE": "?0",
    "HTTP_SEC_CH_UA_PLATFORM": '"Windows"',
    "HTTP_DNT": "1",
    "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
    "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "HTTP_SEC_FETCH_SITE": "same-origin",
    "HTTP_SEC_FETCH_MODE": "navigate",
    "HTTP_SEC_FETCH_USER": "?1",
    "HTTP_SEC_FETCH_DEST": "document",
    "HTTP_REFERER": "http://127.0.0.1:8000/admin/auth/group/",
    "HTTP_ACCEPT_ENCODING": "gzip, deflate, br, zstd",
    "HTTP_ACCEPT_LANGUAGE": "en-GB,en;q=0.9,en-US;q=0.8",
    "HTTP_COOKIE": "sessionid=6uhot0rbw2t5s7swm5tay8mmqr9xq0tx; csrftoken=zLpRBbepoVJAuObJXuL21mKUoNZcrWeg",
}
