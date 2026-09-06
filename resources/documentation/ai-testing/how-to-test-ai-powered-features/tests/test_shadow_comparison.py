import requests

BASE_URL = 'https://staging.qa.local/api/sentiment'


def test_shadow_comparison():
    payload = {'text': 'The app crashes every time I open the settings.'}

    current = requests.post(
        f'{BASE_URL}?model=current',
        json=payload,
        timeout=5
    ).json()

    candidate = requests.post(
        f'{BASE_URL}?model=candidate',
        json=payload,
        timeout=5
    ).json()

    assert current['confidence'] > 0
    assert candidate['confidence'] > 0
    if current['label'] == 'negative':
        assert candidate['confidence'] >= current['confidence'] * 0.9
