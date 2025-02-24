import requests


def add(x, y):
    return x + y


def is_even(x):
    return x % 2 == 0


class API:

    def __init__(self, base_url):
        self.base_url = base_url

    def get_details(self, user_id):
        response = requests.get(f"{self.base_url.rstrip('/')}/{user_id}")
        return response.json


if __name__ == "__main__":
    a = API("https://www.google.com")
    print(a.get_details(23))
