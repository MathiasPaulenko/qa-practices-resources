import requests


class UserService:
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url

    def get_user(self, user_id: int):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def health(self):
        response = requests.get(f"{self.base_url}/health")
        if response.status_code == 503:
            response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json().get("status", "unknown")
