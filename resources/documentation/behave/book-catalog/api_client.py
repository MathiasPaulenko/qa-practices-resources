# api_client.py
import requests


class BookAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get_book(self, title):
        return requests.get(f"{self.base_url}/books/{title}")
