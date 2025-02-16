"""
Construct a class which can effectively handle GET requests. The class should be generic in nature and should be capable of effectively handling headers and payload in the request with proper exception handling mechanisms.

Flow:

1. User creates a GET request and adds header (Optional) and/or payload to the request.

2. This request is sent through an object of the class which parses and checks if the payload and/or header (if exists) is in the correct format.

3. If validated, it then sends this GET request to the API server which was meant for the request and then returns the response.

4. If successful, the response should contain the content as JSON and if not, a user friendly error message should be sent.
"""

import requests
from typing import Dict, Optional, List


# Error List to be implemented in class
# requests.exceptions.URLRequired
# requests.exceptions.InvalidURL
# requests.exceptions.ConnectionError
# requests.exceptions.HTTPError
# requests.exceptions.InvalidHeader
# requests.exceptions.Timeout
class InvalidRequestError(Exception):
    """Handles different request errors."""


class GetHandler:
    """A class to handle GET requests."""

    def __init__(
        self,
        request_url: Optional[str] = None,
        payload: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ):
        self.request_url = request_url
        self.payload = payload if payload else {}
        self.headers = headers if headers else {}

    def valid_request(self, request_url, headers=None, query_params=None):
        """
        Checks if the request is valid. Checks the following:
        - URL: URL should be present and valid.
        - Headers: Headers should be valid.
        - QUery Parameters: Should be a dictionary
        """
        if not request_url or not isinstance(request_url, str):
            raise InvalidRequestError(
                "Invalid URL: The request URL must be a non-empty string."
            )

        if headers and not isinstance(headers, dict):
            raise InvalidRequestError(
                "Invalid Headers: Headers should be a dictionary."
            )

    def build_request(
        self,
        request_url: str,
        headers: Optional[List[Dict]] = None,
        payload: Optional[List[Dict]] = None,
    ):
        """
        Builds the GET request to be sent. Returns a dictionary of arguments if the request is valid.
        """
        self.valid_request(request_url, headers)

        request_data = {
            "url": request_url,
            "headers": headers or {},
            "params": payload
            or {},  # Payload is passed as query parameters in GET requests.
        }
        return request_data

    def get_response(
        self,
        request_url: str,
        headers: Optional[List[Dict]] = None,
        payload: Optional[List[Dict]] = None,
    ):

        try:
            response = requests.get(request_url, timeout=1)
            response.raise_for_status()

            return response

        except (requests.exceptions.URLRequired, requests.exceptions.InvalidURL) as e:
            return f"Please enter a valid URL. \nError: {e}"

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
        ) as e:
            return f"Cannot connect to the server. \nError: {e}"

        except requests.exceptions.InvalidHeader as e:
            return f"One or more header values are not valid. \nError: {e}"

        except requests.exceptions.Timeout as e:
            return f"Connection timed out. \nError: {e}"


obj = GetHandler()
response = obj.get_response("https://catfkact.ninja/facts")
# response = obj.get_response("https://google.com")
print(response.content)

# import requests
# from typing import Dict, Optional


# class RequestErrorHandler(Exception):
#     """Custom exception for request errors."""

#     pass


# class GetHandler:
#     """A class to handle GET requests with proper exception handling."""

#     def __init__(
#         self,
#         request_url: Optional[str] = None,
#         payload: Optional[Dict] = None,
#         headers: Optional[Dict] = None,
#     ):
#         self.request_url = request_url
#         self.payload = payload or {}
#         self.headers = headers or {}

#     def valid_request(self, request_url: str, headers: Optional[Dict] = None):
#         """
#         Checks if the request URL and headers are valid.
#         - URL must be a valid non-empty string.
#         - Headers (if provided) must be a dictionary.
#         """
#         if not request_url or not isinstance(request_url, str):
#             raise RequestErrorHandler(
#                 "Invalid URL: The request URL must be a non-empty string."
#             )

#         if headers and not isinstance(headers, dict):
#             raise RequestErrorHandler(
#                 "Invalid Headers: Headers should be a dictionary."
#             )

#     def build_request(
#         self,
#         request_url: str,
#         headers: Optional[Dict] = None,
#         payload: Optional[Dict] = None,
#     ) -> Dict:
#         """
#         Builds the GET request with URL, headers, and payload.
#         Returns a dictionary containing request parameters if valid.
#         """
#         self.valid_request(request_url, headers)

#         request_data = {
#             "url": request_url,
#             "headers": headers or {},
#             "params": payload
#             or {},  # Payload is passed as query parameters in GET requests.
#         }
#         return request_data

#     def get_response(
#         self,
#         request_url: str,
#         headers: Optional[Dict] = None,
#         payload: Optional[Dict] = None,
#     ):
#         """
#         Sends the GET request and handles exceptions.
#         Returns a JSON response if successful, otherwise returns an error message.
#         """
#         try:
#             request_data = self.build_request(request_url, headers, payload)
#             response = requests.get(**request_data)

#             # Raise an HTTPError for bad responses (4xx and 5xx)
#             response.raise_for_status()

#             return response.json()  # Return JSON response if successful.

#         except requests.exceptions.MissingSchema as e:
#             return {
#                 "error": "Invalid URL format. Ensure it includes 'http://' or 'https://'",
#                 "details": str(e),
#             }

#         except requests.exceptions.InvalidURL as e:
#             return {"error": "Invalid URL provided", "details": str(e)}

#         except requests.exceptions.ConnectionError as e:
#             return {
#                 "error": "Connection error. Unable to reach the server",
#                 "details": str(e),
#             }

#         except requests.exceptions.Timeout as e:
#             return {"error": "Request timed out", "details": str(e)}

#         except requests.exceptions.HTTPError as e:
#             return {
#                 "error": f"HTTP error occurred: {response.status_code}",
#                 "details": str(e),
#             }

#         except requests.exceptions.InvalidHeader as e:
#             return {"error": "Invalid header values provided", "details": str(e)}

#         except requests.exceptions.RequestException as e:
#             return {
#                 "error": "An error occurred while making the request",
#                 "details": str(e),
#             }


# # Example Usage
# if __name__ == "__main__":
#     obj = GetHandler()
#     response = obj.get_response("https://catfact.ninja/fact")  # Corrected the URL typo
#     print(response)
