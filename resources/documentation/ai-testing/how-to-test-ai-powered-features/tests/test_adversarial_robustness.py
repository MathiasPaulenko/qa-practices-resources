import requests

BASE_URL = 'https://staging.qa.local/api/sentiment'

adversarial_inputs = [
    '',                              # empty
    'asdfghjkl',                     # gibberish
    ' ' * 5000,                      # very long
    '???!?!?!',                      # ambiguous punctuation
    'Compra ahora',                  # non-English
    'This is the best worst product ever bought.'  # contradictory
]


def test_adversarial_robustness():
    for text in adversarial_inputs:
        response = requests.post(
            BASE_URL,
            json={'text': text},
            timeout=5
        )
        assert response.status_code in (200, 422)
        if response.status_code == 200:
            data = response.json()
            assert 'label' in data
            assert 0.0 <= data['confidence'] <= 1.0
