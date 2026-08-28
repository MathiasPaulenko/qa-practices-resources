import pytest
from src.user_service import UserService


@pytest.mark.integration
class TestUserServiceIntegration:
    def test_health_against_example(self):
        service = UserService(base_url="https://api.example.com")
        with pytest.raises(Exception):
            service.health()
