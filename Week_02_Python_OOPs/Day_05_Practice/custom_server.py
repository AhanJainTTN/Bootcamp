"""
Construct a class which can effectively handle GET requests. The class should be generic in nature and should be capable of effectively handling headers and payload in the request with proper exception handling mechanisms.

Flow:

1. User creates a GET request and adds header (Optional) and/or payload to the request.

2. This request is sent through an object of the class which parses and checks if the payload and/or header (if exists) is in the correct format.

3. If validated, it then sends this GET request to the API server which was meant for the request and then returns the response.

4. If successful, the response should contain the content as JSON and if not, a user friendly error message should be sent.
"""

# Error List to be implemented in class
# requests.exceptions.URLRequired
# requests.exceptions.InvalidURL
# requests.exceptions.ConnectionError
# requests.exceptions.HTTPError
# requests.exceptions.InvalidHeader
# requests.exceptions.Timeout

import requests
from typing import Dict, Optional


class InvalidRequestError(Exception):
    """Handles different request errors."""


class GetHandler:
    """A class to handle GET requests with proper exception handling."""

    def __init__(
        self,
        request_url: Optional[str] = None,
        payload: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.request_url = request_url
        self.payload = payload or {}
        self.headers = headers or {}

    def valid_request(self, request_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Checks if request is valid.
        - URL: MSst be a non-empty string.
        - Headers: Must be a dictionary.
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
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """
        Builds the GET request payload and headers.
        Returns a dictionary containing request parameters if requesy is valid.
        """
        self.valid_request(request_url, headers)
        request_data = {
            "url": request_url,
            "headers": headers or {},
            "params": payload or {},
            "timeout": 5,
        }
        return request_data

    def get_response(
        self,
        request_url: str,
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, str]] = None,
    ):
        """
        Sends the GET request and handles exceptions.
        Returns JSON response if available, otherwise raw text or error message.
        """

        try:
            request_data = self.build_request(request_url, headers, payload)
            response = requests.get(**request_data)
            response.raise_for_status()

            return response.json()

        # return respone in text format if no JSON response
        except requests.exceptions.JSONDecodeError:
            return response.text

        except (
            requests.exceptions.MissingSchema,
            requests.exceptions.URLRequired,
            requests.exceptions.InvalidURL,
        ) as e:
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


def main():
    obj = GetHandler()
    response1 = obj.get_response("invalid_url")
    print(response1)
    response2 = obj.get_response("http://invalid-url")
    print(response2)
    response3 = obj.get_response("http://googelr.com")
    print(response3)
    response4 = obj.get_response("http://128.255.255.1")
    print(response4)
    response5 = obj.get_response("https://catfact.ninja/fact")
    print(response5)
    response6 = obj.get_response("https://google.com")
    print(response6)


if __name__ == "__main__":
    main()
