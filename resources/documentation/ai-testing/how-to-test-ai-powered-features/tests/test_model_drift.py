import json
import requests

BASE_URL = 'https://staging.qa.local/api/sentiment'


def compute_f1(golden, predictions):
    tp = sum(1 for g, p in zip(golden, predictions) if g == p)
    fp = sum(1 for g, p in zip(golden, predictions) if g != p and p in set(golden))
    fn = sum(1 for g, p in zip(golden, predictions) if g != p and g not in set(golden))
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    return 2 * precision * recall / (precision + recall) if (precision + recall) else 0


def test_model_drift():
    with open('tests/golden-dataset.json') as f:
        dataset = json.load(f)

    predictions = []
    for item in dataset:
        response = requests.post(
            BASE_URL,
            json={'text': item['input']},
            timeout=5
        )
        predictions.append(response.json()['label'])

    labels = [item['expected_label'][0] for item in dataset]
    f1 = compute_f1(labels, predictions)
    assert f1 >= 0.92, f'F1 score {f1} below baseline 0.92'
