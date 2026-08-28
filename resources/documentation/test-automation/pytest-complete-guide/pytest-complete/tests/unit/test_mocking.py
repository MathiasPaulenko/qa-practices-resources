import pytest
from src.user_service import UserService


def test_get_user_with_mock(mocker):
    mock_response = {"id": 1, "name": "Jane Doe", "email": "jane@example.com"}
    mocker.patch.object(UserService, "get_user", return_value=mock_response)

    user = UserService().get_user(1)
    assert user["name"] == "Jane Doe"
    assert user["email"] == "jane@example.com"


def test_health_api_down(mocker):
    mock_get = mocker.patch("src.user_service.requests.get")
    mock_get.side_effect = ConnectionError("API unreachable")

    with pytest.raises(ConnectionError):
        UserService().health()


def test_health_retry(mocker):
    mock_get = mocker.patch("src.user_service.requests.get")
    mock_get.side_effect = [
        type("Response", (), {"status_code": 503, "json": lambda: {"status": "down"}})(),
        type("Response", (), {"status_code": 200, "json": lambda: {"status": "ok"}})(),
    ]

    status = UserService().health()
    assert status == "ok"
    assert mock_get.call_count == 2
