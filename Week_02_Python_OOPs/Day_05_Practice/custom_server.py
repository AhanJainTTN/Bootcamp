import requests
import os


class ResourceNotFoundError(Exception):
    """
    Raises an exception if the resource is not found.
    """

    def __str__(self) -> str:
        return (
            f"Invalid request endpoint. Please use the below endpoints: \nfacts\nbreeds"
        )


class BadRequestError(Exception):
    """
    Raises an exception if the parameters are not valid.
    """

    def __str__(self) -> str:
        return f"Invalid request parameter."


class InvalidTokenError(Exception):
    """
    Raises an exception if the token is not valid.
    """

    def __str__(self) -> str:
        return f"Invalid token."


class MyServer:
    """
    MyServer is a simple HTTP server which can handle GET requests. To simulate internal data processing and retrieval, it gets data from the 'catfact' API.
    """

    base_url = "https://catfact.ninja/"
    valid_tokens = {"a", "b", "c"}

    # def __init__(self, token):
    #     try:
    #         if token not in self.valid_tokens:
    #             raise InvalidTokenError
    #     except InvalidTokenError as e:
    #         print(f"Error: {e}")

    def handle_get(self, resource_endpoint, query_params=None):
        """
        Parent function to handle requests and redirects requests to other class functions.
        """
        try:
            self.query_string = self.process_query_params(query_params)
            if os.path.basename(resource_endpoint).split("?")[0] == "facts":
                print(self.query_string)
                return self.handle_get_facts()
            elif os.path.basename(resource_endpoint).split("?")[0] == "breeds":
                return self.handle_get_breeds()
            raise ResourceNotFoundError
        except ResourceNotFoundError as e:
            print(f"Error: {e}")

    def process_query_params(self, query_params=None):
        """
        Function to process query parameters. Returns a parsed query string.
        """
        if not query_params:
            return

        self.query_string = "?"

        try:
            for key, value in query_params.items():
                if key not in {"limit"}:
                    raise BadRequestError
                self.query_string += f"{key}={value}&"
            self.query_string.rstrip("&")
        except BadRequestError as e:
            print(f"Error: {e}")

    def handle_get_facts(self):
        """
        Handle get requests when user requests for facts.
        """
        if not self.query_string:
            request_url = os.path.join(self.base_url, "facts")
            response = requests.get(request_url)
        else:
            request_url = os.path.join(self.base_url, "facts", self.query_string)
            response = requests.get(request_url)

        return response.content

    def handle_get_all_breeds(self):
        """
        Handle get requests when user requests for breeds.
        """
        request_url = os.path.join(self.base_url, "breeds")
        response = requests.get(request_url)

        return response.content


cat_fact_obj = MyServer()
# print(cat_fact_obj.handle_get("factss"))
# print(cat_fact_obj.handle_get("breedzs"))
query_params = {"limit": 2}
print(cat_fact_obj.handle_get("facts", query_params))
# print(cat_fact_obj.handle_get("breeds"))
