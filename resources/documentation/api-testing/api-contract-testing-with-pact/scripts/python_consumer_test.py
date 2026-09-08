# python_consumer_test.py
# Requires: pact-python 2.x, requests 2.32
import requests
from pact import Pact, match

pact = Pact('billing-service', 'user-service')

def test_get_user():
    expected = {
        'id': match.int(123),
        'name': match.str('Jane Doe'),
        'email': match.str('jane@qa.local')
    }

    (
        pact
        .given('user with id 123 exists')
        .upon_receiving('a request for user 123')
        .with_request('GET', '/users/123', headers={'Accept': 'application/json'})
        .will_respond_with(200, body=expected)
    )

    with pact.serve() as srv:
        result = requests.get(f'{srv.url}/users/123').json()
        assert result['id'] == 123
