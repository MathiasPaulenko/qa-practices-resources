import requests

BASE_URL = 'https://staging.qa.local/api/sentiment'


def test_model_contract():
    response = requests.post(
        BASE_URL,
        json={'text': 'Great product, fast delivery.'},
        timeout=5
    )

    assert response.status_code == 200
    data = response.json()
    assert 'label' in data
    assert 'confidence' in data
    assert data['label'] in ['positive', 'negative', 'mixed']
    assert 0.0 <= data['confidence'] <= 1.0
    assert response.elapsed.total_seconds() < 0.5
