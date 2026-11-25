import requests
import json


class CustomLibrary:
    """Example Robot Framework library exposing HTTP helpers as keywords."""

    def get_api_response(self, url):
        """Fetch API response and return status code."""
        response = requests.get(url)
        return response.status_code

    def post_api_data(self, url, data):
        """POST data to API and return response."""
        response = requests.post(url, json=json.loads(data))
        return response.json()

    def validate_json_field(self, json_string, field, expected_value):
        """Validate a field in a JSON response."""
        data = json.loads(json_string)
        actual_value = data.get(field)
        if str(actual_value) != str(expected_value):
            raise AssertionError(
                f"Field '{field}' expected '{expected_value}' but got '{actual_value}'"
            )
