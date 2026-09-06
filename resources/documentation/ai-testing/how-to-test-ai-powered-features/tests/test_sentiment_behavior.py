import json
import requests

BASE_URL = 'https://staging.qa.local/api/sentiment'


def test_sentiment_behavior(golden_item):
    response = requests.post(
        BASE_URL,
        json={'text': golden_item['input']},
        timeout=5
    )
    data = response.json()

    assert data['label'] in golden_item['expected_label']
    assert data['confidence'] >= golden_item['min_confidence']
    assert response.elapsed.total_seconds() * 1000 < golden_item['max_latency_ms']


def load_golden_dataset():
    with open('tests/golden-dataset.json') as f:
        return json.load(f)


import pytest

@pytest.fixture(params=load_golden_dataset())
def golden_item(request):
    return request.param
